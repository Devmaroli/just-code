/**
 * ReplaceFootageBySize.jsx
 * Adobe After Effects ExtendScript (ScriptUI)
 *
 * Pick a folder in the panel. The script finds images and videos already
 * in the project, matches them to files in that folder by pixel size
 * (width × height), and replaces the project footage with the folder files.
 *
 * Install either way:
 *   File > Scripts > Run Script File…
 *   or copy into Scripts/ScriptUI Panels and open it from Window.
 *
 * Preferences > Scripting & Expressions:
 *   enable “Allow Scripts to Write Files and Access Network”
 */

#target aftereffects

(function ReplaceFootageBySize(thisObj) {
    var SCRIPT_TITLE = "Replace Footage by Size";
    var TEMP_FOLDER_NAME = "_ReplaceFootageBySize_Temp";

    var IMAGE_EXTS = {
        jpg: 1, jpeg: 1, png: 1, tif: 1, tiff: 1, gif: 1, bmp: 1,
        psd: 1, psb: 1, tga: 1, exr: 1, dpx: 1, hdr: 1, webp: 1,
        heic: 1, svg: 1, jfif: 1, iff: 1, rla: 1, rpf: 1
    };
    var VIDEO_EXTS = {
        mp4: 1, mov: 1, avi: 1, mxf: 1, m4v: 1, mpg: 1, mpeg: 1,
        wmv: 1, mkv: 1, r3d: 1, braw: 1, webm: 1, ts: 1, mts: 1,
        m2ts: 1, "3gp": 1, flv: 1, f4v: 1, ogv: 1
    };

    var state = {
        folder: null,
        matches: [],
        unmatchedProject: [],
        unmatchedFolder: [],
        errors: []
    };

    // -------------------------------------------------------------------------
    // Helpers
    // -------------------------------------------------------------------------

    function trimStr(s) {
        return String(s).replace(/^\s+|\s+$/g, "");
    }

    function lower(s) {
        return String(s).toLowerCase();
    }

    function fileExt(name) {
        var n = String(name);
        var i = n.lastIndexOf(".");
        if (i < 0) {
            return "";
        }
        return lower(n.substring(i + 1));
    }

    function baseName(name) {
        var n = String(name);
        var slash = Math.max(n.lastIndexOf("/"), n.lastIndexOf("\\"));
        if (slash >= 0) {
            n = n.substring(slash + 1);
        }
        var i = n.lastIndexOf(".");
        if (i > 0) {
            n = n.substring(0, i);
        }
        return n;
    }

    function sizeKey(w, h) {
        return String(Math.round(w)) + "x" + String(Math.round(h));
    }

    function kindFromStill(isStill, ext) {
        if (isStill === true) {
            return "Image";
        }
        if (isStill === false) {
            return "Video";
        }
        if (IMAGE_EXTS[ext]) {
            return "Image";
        }
        if (VIDEO_EXTS[ext]) {
            return "Video";
        }
        return "Media";
    }

    function isMediaFile(file) {
        if (!(file instanceof File) || file.hidden) {
            return false;
        }
        var ext = fileExt(file.name);
        if (!ext || ext === "ds_store" || ext === "db") {
            return false;
        }
        return !!(IMAGE_EXTS[ext] || VIDEO_EXTS[ext]);
    }

    function isWantedKind(kind, includeImages, includeVideos) {
        if (kind === "Image") {
            return includeImages;
        }
        if (kind === "Video") {
            return includeVideos;
        }
        return includeImages || includeVideos;
    }

    function safeFsName(file) {
        try {
            return file.fsName;
        } catch (e) {
            return "";
        }
    }

    function sameFile(a, b) {
        if (!a || !b) {
            return false;
        }
        return lower(safeFsName(a)) === lower(safeFsName(b));
    }

    function nameScore(projectName, projectFile, folderFile) {
        var p = lower(baseName(projectName));
        var pf = projectFile ? lower(baseName(projectFile.name)) : "";
        var f = lower(baseName(folderFile.name));
        if (!f) {
            return 0;
        }
        if (pf && pf === f) {
            return 100;
        }
        if (p === f) {
            return 90;
        }
        if (p.indexOf(f) >= 0 || f.indexOf(p) >= 0) {
            return 50;
        }
        if (pf && (pf.indexOf(f) >= 0 || f.indexOf(pf) >= 0)) {
            return 40;
        }
        return 0;
    }

    function collectMediaFiles(folder, recursive, out) {
        if (!folder || !(folder instanceof Folder)) {
            return out;
        }
        var entries;
        try {
            entries = folder.getFiles();
        } catch (e) {
            state.errors.push("Could not read folder: " + folder.fsName);
            return out;
        }
        if (!entries) {
            return out;
        }
        for (var i = 0; i < entries.length; i++) {
            var entry = entries[i];
            if (entry instanceof Folder) {
                if (recursive && entry.name !== "." && entry.name !== "..") {
                    collectMediaFiles(entry, recursive, out);
                }
            } else if (isMediaFile(entry)) {
                out.push(entry);
            }
        }
        return out;
    }

    function isPlaceholderFootage(item) {
        return item instanceof FootageItem &&
            item.mainSource &&
            item.mainSource instanceof PlaceholderSource;
    }

    function isSolidFootage(item) {
        return item instanceof FootageItem &&
            item.mainSource &&
            item.mainSource instanceof SolidSource;
    }

    function footageKind(item) {
        if (isSolidFootage(item) || isPlaceholderFootage(item)) {
            return "Placeholder";
        }
        try {
            if (item.mainSource && item.mainSource.isStill) {
                return "Image";
            }
            return "Video";
        } catch (e) {
            return kindFromStill(null, item.file ? fileExt(item.file.name) : "");
        }
    }

    function walkProjectItems(items, visit) {
        for (var i = 1; i <= items.length; i++) {
            var item = items[i];
            if (item instanceof FolderItem) {
                if (item.name === TEMP_FOLDER_NAME) {
                    continue;
                }
                walkProjectItems(item.items, visit);
            } else {
                visit(item);
            }
        }
    }

    function getActiveComp() {
        var item = app.project.activeItem;
        if (item && item instanceof CompItem) {
            return item;
        }
        return null;
    }

    function collectTargetFootage(targetMode, includeImages, includeVideos, includePlaceholders) {
        var found = [];
        var seen = {};

        function consider(item) {
            if (!item || !(item instanceof FootageItem)) {
                return;
            }
            if (seen[item.id]) {
                return;
            }
            var kind = footageKind(item);
            if (kind === "Placeholder") {
                if (!includePlaceholders) {
                    return;
                }
            } else if (!isWantedKind(kind, includeImages, includeVideos)) {
                return;
            }
            if (!item.width || !item.height) {
                return;
            }
            seen[item.id] = true;
            found.push(item);
        }

        if (targetMode === "selected") {
            var sel = app.project.selection;
            if (sel) {
                for (var s = 0; s < sel.length; s++) {
                    consider(sel[s]);
                }
            }
            return found;
        }

        if (targetMode === "comp") {
            var comp = getActiveComp();
            if (!comp) {
                return found;
            }
            for (var L = 1; L <= comp.numLayers; L++) {
                try {
                    consider(comp.layer(L).source);
                } catch (e) {}
            }
            return found;
        }

        walkProjectItems(app.project.items, consider);
        return found;
    }

    function findTempFolder() {
        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            if (item instanceof FolderItem && item.name === TEMP_FOLDER_NAME) {
                return item;
            }
        }
        return null;
    }

    function removeTempFolder() {
        var folder = findTempFolder();
        if (!folder) {
            return;
        }
        try {
            folder.remove();
        } catch (e) {
            try {
                while (folder.numItems > 0) {
                    folder.item(1).remove();
                }
                folder.remove();
            } catch (e2) {}
        }
    }

    function getOrCreateTempFolder() {
        var folder = findTempFolder();
        if (folder) {
            return folder;
        }
        return app.project.items.addFolder(TEMP_FOLDER_NAME);
    }

    function importFolderAsset(file, tempFolder) {
        var io;
        try {
            io = new ImportOptions(file);
        } catch (e) {
            return null;
        }
        try {
            if (!io.canImportAs(ImportAsType.FOOTAGE)) {
                return null;
            }
            io.importAs = ImportAsType.FOOTAGE;
            io.sequence = false;
        } catch (e2) {
            return null;
        }

        var imported = null;
        var suppressed = false;
        try {
            app.beginSuppressDialogs();
            suppressed = true;
            imported = app.project.importFile(io);
        } catch (e3) {
            imported = null;
        }
        if (suppressed) {
            try {
                app.endSuppressDialogs(false);
            } catch (e4) {}
        }
        if (!imported || !(imported instanceof FootageItem)) {
            return null;
        }
        try {
            imported.parentFolder = tempFolder;
        } catch (e5) {}
        return imported;
    }

    function readFolderAssets(files, onProgress) {
        var assets = [];
        app.beginUndoGroup(SCRIPT_TITLE + " (read sizes)");
        try {
            var tempFolder = getOrCreateTempFolder();

            for (var i = 0; i < files.length; i++) {
                if (onProgress) {
                    onProgress(i + 1, files.length, files[i].name);
                }
                var imported = importFolderAsset(files[i], tempFolder);
                if (!imported) {
                    state.errors.push("Could not read: " + files[i].name);
                    continue;
                }
                var ext = fileExt(files[i].name);
                var isStill = false;
                try {
                    isStill = !!(imported.mainSource && imported.mainSource.isStill);
                } catch (e) {
                    isStill = !!IMAGE_EXTS[ext];
                }
                assets.push({
                    file: files[i],
                    name: files[i].name,
                    width: imported.width,
                    height: imported.height,
                    kind: kindFromStill(isStill, ext),
                    size: sizeKey(imported.width, imported.height)
                });
            }

            removeTempFolder();
        } catch (eRead) {
            try {
                removeTempFolder();
            } catch (eCleanup) {}
            state.errors.push("Scan stopped: " + eRead.toString());
        }
        app.endUndoGroup();
        return assets;
    }

    function projectRecord(item) {
        var file = null;
        try {
            file = item.file;
        } catch (e) {
            file = null;
        }
        return {
            item: item,
            id: item.id,
            name: item.name,
            width: item.width,
            height: item.height,
            size: sizeKey(item.width, item.height),
            kind: footageKind(item),
            file: file
        };
    }

    function buildMatches(projectItems, folderAssets, matchMode, reuseSameSize) {
        var matches = [];
        var usedProject = {};
        var usedFolder = {};

        function addMatch(proj, asset, reason) {
            if (usedProject[proj.id]) {
                return;
            }
            if (!reuseSameSize && usedFolder[safeFsName(asset.file)]) {
                return;
            }
            if (sameFile(proj.file, asset.file)) {
                return;
            }
            usedProject[proj.id] = true;
            usedFolder[safeFsName(asset.file)] = true;
            matches.push({
                project: proj,
                asset: asset,
                reason: reason
            });
        }

        function matchByName(onlyUnused) {
            for (var i = 0; i < projectItems.length; i++) {
                var proj = projectItems[i];
                if (onlyUnused && usedProject[proj.id]) {
                    continue;
                }
                var best = null;
                var bestScore = 0;
                for (var j = 0; j < folderAssets.length; j++) {
                    var asset = folderAssets[j];
                    if (!reuseSameSize && usedFolder[safeFsName(asset.file)]) {
                        continue;
                    }
                    var score = nameScore(proj.name, proj.file, asset.file);
                    if (score > bestScore) {
                        bestScore = score;
                        best = asset;
                    }
                }
                if (best && bestScore >= 90) {
                    addMatch(proj, best, "name");
                }
            }
        }

        function matchBySize() {
            var groups = {};
            var i;
            for (i = 0; i < folderAssets.length; i++) {
                var key = folderAssets[i].size;
                if (!groups[key]) {
                    groups[key] = { project: [], folder: [] };
                }
                groups[key].folder.push(folderAssets[i]);
            }
            for (i = 0; i < projectItems.length; i++) {
                if (usedProject[projectItems[i].id]) {
                    continue;
                }
                var pkey = projectItems[i].size;
                if (!groups[pkey]) {
                    groups[pkey] = { project: [], folder: [] };
                }
                groups[pkey].project.push(projectItems[i]);
            }

            for (var size in groups) {
                if (!groups.hasOwnProperty(size)) {
                    continue;
                }
                var group = groups[size];
                var remainingP = [];
                var p;
                for (p = 0; p < group.project.length; p++) {
                    if (!usedProject[group.project[p].id]) {
                        remainingP.push(group.project[p]);
                    }
                }
                var remainingF = [];
                var f;
                for (f = 0; f < group.folder.length; f++) {
                    if (reuseSameSize || !usedFolder[safeFsName(group.folder[f].file)]) {
                        remainingF.push(group.folder[f]);
                    }
                }
                if (!remainingP.length || !remainingF.length) {
                    continue;
                }

                if (reuseSameSize && remainingF.length === 1) {
                    for (p = 0; p < remainingP.length; p++) {
                        addMatch(remainingP[p], remainingF[0], "size");
                    }
                    continue;
                }

                var pairs = [];
                for (p = 0; p < remainingP.length; p++) {
                    for (f = 0; f < remainingF.length; f++) {
                        pairs.push({
                            project: remainingP[p],
                            asset: remainingF[f],
                            score: nameScore(remainingP[p].name, remainingP[p].file, remainingF[f].file)
                        });
                    }
                }
                pairs.sort(function (a, b) {
                    return b.score - a.score;
                });

                for (i = 0; i < pairs.length; i++) {
                    addMatch(pairs[i].project, pairs[i].asset, pairs[i].score >= 40 ? "size+name" : "size");
                }

                if (reuseSameSize && remainingF.length) {
                    for (p = 0; p < remainingP.length; p++) {
                        if (!usedProject[remainingP[p].id]) {
                            addMatch(remainingP[p], remainingF[0], "size");
                        }
                    }
                }
            }
        }

        if (matchMode === "name") {
            matchByName(false);
        } else if (matchMode === "sizeAndName") {
            matchBySize();
            var kept = [];
            for (var k = 0; k < matches.length; k++) {
                if (matches[k].reason === "size+name" || matches[k].reason === "name") {
                    kept.push(matches[k]);
                } else {
                    usedProject[matches[k].project.id] = false;
                    usedFolder[safeFsName(matches[k].asset.file)] = false;
                }
            }
            matches = kept;
        } else {
            // size (default): match pixel size, prefer a file-name tie-break
            matchBySize();
        }

        var unmatchedProject = [];
        var unmatchedFolder = [];
        var m;
        for (m = 0; m < projectItems.length; m++) {
            if (!usedProject[projectItems[m].id]) {
                unmatchedProject.push(projectItems[m]);
            }
        }
        for (m = 0; m < folderAssets.length; m++) {
            if (!usedFolder[safeFsName(folderAssets[m].file)]) {
                unmatchedFolder.push(folderAssets[m]);
            }
        }

        return {
            matches: matches,
            unmatchedProject: unmatchedProject,
            unmatchedFolder: unmatchedFolder
        };
    }

    function applyReplacements(matches) {
        var replaced = 0;
        var failed = [];
        app.beginUndoGroup(SCRIPT_TITLE);
        try {
            for (var i = 0; i < matches.length; i++) {
                var pair = matches[i];
                try {
                    pair.project.item.replace(pair.asset.file);
                    replaced++;
                } catch (e) {
                    failed.push(pair.project.name + " → " + pair.asset.name + " (" + e.toString() + ")");
                }
            }
        } finally {
            app.endUndoGroup();
        }
        return { replaced: replaced, failed: failed };
    }

    // -------------------------------------------------------------------------
    // UI
    // -------------------------------------------------------------------------

    function setStatus(ui, text) {
        ui.status.text = text;
    }

    function refreshList(ui) {
        ui.list.removeAll();
        for (var i = 0; i < state.matches.length; i++) {
            var pair = state.matches[i];
            var line = pair.project.size + "  " +
                pair.project.name + "  →  " +
                pair.asset.name +
                "  (" + pair.reason + ", " + pair.asset.kind + ")";
            ui.list.add("item", line);
        }
        var extra = [];
        extra.push(state.matches.length + " match" + (state.matches.length === 1 ? "" : "es"));
        extra.push(state.unmatchedProject.length + " unmatched project item" + (state.unmatchedProject.length === 1 ? "" : "s"));
        extra.push(state.unmatchedFolder.length + " unused folder file" + (state.unmatchedFolder.length === 1 ? "" : "s"));
        if (state.errors.length) {
            extra.push(state.errors.length + " read error" + (state.errors.length === 1 ? "" : "s"));
        }
        ui.summary.text = extra.join("  ·  ");
        ui.replaceBtn.enabled = state.matches.length > 0;
    }

    function selectedMatches(ui) {
        if (!ui.list.selection) {
            return state.matches;
        }
        var sel = ui.list.selection;
        if (!(sel instanceof Array)) {
            sel = [sel];
        }
        if (!sel.length) {
            return state.matches;
        }
        var out = [];
        for (var i = 0; i < sel.length; i++) {
            if (typeof sel[i].index === "number" && state.matches[sel[i].index]) {
                out.push(state.matches[sel[i].index]);
            }
        }
        return out.length ? out : state.matches;
    }

    function onBrowse(ui) {
        var start = state.folder || Folder.desktop;
        var picked = Folder.selectDialog("Choose a folder of replacement images or videos", start);
        if (picked) {
            state.folder = picked;
            ui.path.text = picked.fsName;
            setStatus(ui, "Folder set. Click Scan & Preview.");
        }
    }

    function currentMatchMode(ui) {
        if (ui.matchName.value) {
            return "name";
        }
        if (ui.matchBoth.value) {
            return "sizeAndName";
        }
        return "size";
    }

    function currentTargetMode(ui) {
        if (ui.targetSelected.value) {
            return "selected";
        }
        if (ui.targetComp.value) {
            return "comp";
        }
        return "all";
    }

    function onScan(ui) {
        state.matches = [];
        state.unmatchedProject = [];
        state.unmatchedFolder = [];
        state.errors = [];

        if (!app.project) {
            alert("Open an After Effects project first.");
            return;
        }
        if (!state.folder || !state.folder.exists) {
            alert("Choose a folder that contains the replacement images or videos.");
            return;
        }
        if (!ui.includeImages.value && !ui.includeVideos.value && !ui.includePlaceholders.value) {
            alert("Turn on at least one material type: Images, Videos, or Placeholders.");
            return;
        }

        var files = collectMediaFiles(state.folder, ui.subfolders.value, []);
        if (!files.length) {
            refreshList(ui);
            setStatus(ui, "No images or videos found in that folder.");
            alert("No supported image or video files were found in:\n" + state.folder.fsName);
            return;
        }

        var projectItems = collectTargetFootage(
            currentTargetMode(ui),
            ui.includeImages.value,
            ui.includeVideos.value,
            ui.includePlaceholders.value
        );
        if (!projectItems.length) {
            refreshList(ui);
            setStatus(ui, "No matching footage in the project for the current target.");
            alert("No project images/videos matched the current target filters.");
            return;
        }

        var records = [];
        for (var i = 0; i < projectItems.length; i++) {
            records.push(projectRecord(projectItems[i]));
        }

        setStatus(ui, "Reading folder files to get pixel sizes…");
        if (ui.win.layout && ui.win.layout.layout) {
            ui.win.layout.layout(true);
        }
        if (ui.win.update) {
            ui.win.update();
        }

        var assets = readFolderAssets(files, function (n, total, name) {
            setStatus(ui, "Reading " + n + "/" + total + ": " + name);
            if (ui.win.update) {
                ui.win.update();
            }
        });

        var result = buildMatches(
            records,
            assets,
            currentMatchMode(ui),
            ui.reuse.value
        );
        state.matches = result.matches;
        state.unmatchedProject = result.unmatchedProject;
        state.unmatchedFolder = result.unmatchedFolder;

        refreshList(ui);

        var msg = "Preview ready: " + state.matches.length + " replacement" +
            (state.matches.length === 1 ? "" : "s") + " planned.";
        if (state.errors.length) {
            msg += " " + state.errors.length + " file(s) could not be read.";
        }
        setStatus(ui, msg);
    }

    function onReplace(ui) {
        if (!state.matches.length) {
            alert("Scan a folder first so matches can be previewed.");
            return;
        }
        var toApply = selectedMatches(ui);
        var result = applyReplacements(toApply);
        var msg = "Replaced " + result.replaced + " item" + (result.replaced === 1 ? "" : "s") + ".";
        if (result.failed.length) {
            msg += " " + result.failed.length + " failed.";
            alert(msg + "\n\n" + result.failed.join("\n"));
        }
        setStatus(ui, msg);

        // Drop applied rows from the preview
        if (result.replaced) {
            var appliedIds = {};
            for (var i = 0; i < toApply.length; i++) {
                appliedIds[toApply[i].project.id] = true;
            }
            var remaining = [];
            for (var j = 0; j < state.matches.length; j++) {
                if (!appliedIds[state.matches[j].project.id]) {
                    remaining.push(state.matches[j]);
                }
            }
            state.matches = remaining;
            refreshList(ui);
        }
    }

    function onReset(ui) {
        state.folder = null;
        state.matches = [];
        state.unmatchedProject = [];
        state.unmatchedFolder = [];
        state.errors = [];
        ui.path.text = "";
        refreshList(ui);
        setStatus(ui, "Choose a folder of replacement images or videos.");
        try {
            removeTempFolder();
        } catch (e) {}
    }

    function buildUI(thisObj) {
        var win = (thisObj instanceof Panel)
            ? thisObj
            : new Window("palette", SCRIPT_TITLE, undefined, { resizeable: true });

        win.orientation = "column";
        win.alignChildren = ["fill", "top"];
        win.spacing = 8;
        win.margins = 12;

        var folderPanel = win.add("panel", undefined, "Replacement folder");
        folderPanel.orientation = "column";
        folderPanel.alignChildren = ["fill", "top"];
        folderPanel.margins = 12;
        folderPanel.spacing = 8;

        var pathRow = folderPanel.add("group");
        pathRow.orientation = "row";
        pathRow.alignChildren = ["fill", "center"];
        var path = pathRow.add("edittext", undefined, "");
        path.alignment = ["fill", "center"];
        path.preferredSize = [320, 24];
        var browseBtn = pathRow.add("button", undefined, "Browse…");
        browseBtn.alignment = ["right", "center"];
        browseBtn.preferredSize = [90, 26];

        var subfolders = folderPanel.add("checkbox", undefined, "Include subfolders");
        subfolders.value = true;

        var matchPanel = win.add("panel", undefined, "Match");
        matchPanel.orientation = "column";
        matchPanel.alignChildren = ["left", "top"];
        matchPanel.margins = 12;
        matchPanel.spacing = 4;
        var matchSize = matchPanel.add("radiobutton", undefined, "Pixel size (width × height)");
        var matchName = matchPanel.add("radiobutton", undefined, "File name (ignore extension)");
        var matchBoth = matchPanel.add("radiobutton", undefined, "Both size and file name");
        matchSize.value = true;

        var targetPanel = win.add("panel", undefined, "Project items to replace");
        targetPanel.orientation = "column";
        targetPanel.alignChildren = ["left", "top"];
        targetPanel.margins = 12;
        targetPanel.spacing = 4;
        var targetAll = targetPanel.add("radiobutton", undefined, "All project footage");
        var targetSelected = targetPanel.add("radiobutton", undefined, "Selected project items");
        var targetComp = targetPanel.add("radiobutton", undefined, "Footage used in the active composition");
        targetAll.value = true;

        var typeRow = targetPanel.add("group");
        typeRow.orientation = "row";
        var includeImages = typeRow.add("checkbox", undefined, "Images");
        var includeVideos = typeRow.add("checkbox", undefined, "Videos");
        var includePlaceholders = typeRow.add("checkbox", undefined, "Placeholders / solids");
        includeImages.value = true;
        includeVideos.value = true;
        includePlaceholders.value = true;

        var reuse = targetPanel.add("checkbox", undefined, "Reuse one folder file for every same-size item");
        reuse.value = true;

        var scanBtn = win.add("button", undefined, "Scan & Preview");

        var list = win.add("listbox", undefined, [], { multiselect: true });
        list.preferredSize = [460, 160];
        list.alignment = ["fill", "fill"];

        var summary = win.add("statictext", undefined, "No scan yet.");
        summary.characters = 70;

        var actionRow = win.add("group");
        actionRow.orientation = "row";
        actionRow.alignChildren = ["left", "center"];
        var replaceBtn = actionRow.add("button", undefined, "Replace Matches");
        replaceBtn.enabled = false;
        var resetBtn = actionRow.add("button", undefined, "Reset");

        var status = win.add("statictext", undefined, "Choose a folder of replacement images or videos.");
        status.characters = 70;

        var help = win.add(
            "statictext",
            undefined,
            "Tip: select rows to replace only those matches. Leave none selected to replace all.",
            { multiline: true }
        );
        help.preferredSize = [460, 28];

        var ui = {
            win: win,
            path: path,
            subfolders: subfolders,
            matchSize: matchSize,
            matchName: matchName,
            matchBoth: matchBoth,
            targetAll: targetAll,
            targetSelected: targetSelected,
            targetComp: targetComp,
            includeImages: includeImages,
            includeVideos: includeVideos,
            includePlaceholders: includePlaceholders,
            reuse: reuse,
            list: list,
            summary: summary,
            replaceBtn: replaceBtn,
            status: status
        };

        browseBtn.onClick = function () {
            onBrowse(ui);
        };
        path.onChange = function () {
            var text = trimStr(path.text);
            if (!text) {
                state.folder = null;
                return;
            }
            var folder = new Folder(text);
            if (folder.exists) {
                state.folder = folder;
                setStatus(ui, "Folder set. Click Scan & Preview.");
            } else {
                state.folder = null;
                setStatus(ui, "That folder path does not exist.");
            }
        };
        scanBtn.onClick = function () {
            onScan(ui);
        };
        replaceBtn.onClick = function () {
            onReplace(ui);
        };
        resetBtn.onClick = function () {
            onReset(ui);
        };

        win.onResizing = win.onResize = function () {
            this.layout.resize();
        };
        win.layout.layout(true);
        win.layout.resize();

        return win;
    }

    var panel = buildUI(thisObj);
    if (panel instanceof Window) {
        panel.center();
        panel.show();
    } else {
        panel.layout.layout(true);
        panel.layout.resize();
    }
})(this);

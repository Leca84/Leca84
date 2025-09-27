<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bash Terminal Emulator</title>
    <link rel="stylesheet" href="https://unpkg.com/xterm/css/xterm.css">
    <style>
        :root {
            --bg-color: #1e1e1e;
            --terminal-bg: #000000;
            --terminal-border: #4CAF50;
            --text-color: #ffffff;
            --prompt-color: #4CAF50;
            --command-color: #ff9800;
            --error-color: #f44336;
        }
        
        body {
            margin: 0;
            padding: 20px;
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Courier New', monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        
        .container {
            width: 95%;
            max-width: 1000px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        
        #terminal {
            border: 2px solid var(--terminal-border);
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        
        .controls {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }
        
        button {
            background: var(--terminal-border);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-family: inherit;
        }
        
        button:hover {
            opacity: 0.9;
        }
        
        .info-panel {
            background: #2d2d2d;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Bash Terminal Emulator</h1>
            <p>Эмуляция Linux терминала в браузере</p>
        </div>
        
        <div id="terminal"></div>
        
        <div class="controls">
            <button onclick="clearTerminal()">Очистить</button>
            <button onclick="showHelp()">Помощь</button>
            <button onclick="insertCommand('ls -la')">Вставить ls</button>
            <button onclick="insertCommand('cat README.md')">Вставить cat</button>
        </div>
        
        <div class="info-panel">
            <p><strong>Доступные команды:</strong> ls, cd, cat, pwd, whoami, date, echo, mkdir, touch, rm, help, clear</p>
            <p><strong>Особенности:</strong> история команд, автодополнение (Tab), поддержка стрелок</p>
        </div>
    </div>

    <script src="https://unpkg.com/xterm/lib/xterm.js"></script>
    <script src="https://unpkg.com/xterm-addon-fit/lib/xterm-addon-fit.js"></script>
    <script src="https://unpkg.com/xterm-addon-web-links/lib/xterm-addon-web-links.js"></script>
    
    <script>
        // Инициализация терминала
        const terminal = new Terminal({
            cursorBlink: true,
            fontSize: 14,
            fontFamily: "'Courier New', monospace",
            theme: {
                background: '#000000',
                foreground: '#ffffff',
                cursor: '#4CAF50',
                selection: '#4CAF50'
            }
        });
        
        const fitAddon = new FitAddon.FitAddon();
        const webLinksAddon = new WebLinksAddon.WebLinksAddon();
        
        terminal.loadAddon(fitAddon);
        terminal.loadAddon(webLinksAddon);
        terminal.open(document.getElementById('terminal'));
        fitAddon.fit();
        
        // Переменные состояния
        let currentPath = '/home/user';
        let commandHistory = [];
        let historyIndex = -1;
        let currentCommand = '';
        let fileSystem = {
            '/home/user': {
                'README.md': '# Добро пожаловать!\n\nЭто эмуляция файловой системы.\n',
                'documents': {
                    'notes.txt': 'Важные заметки...\n'
                },
                'projects': {
                    'website': {
                        'index.html': '<html>\n<body>\n  <h1>Мой сайт</h1>\n</body>\n</html>'
                    }
                }
            }
        };
        
        // Приветственное сообщение
        terminal.writeln('Добро пожаловать в Bash Terminal Emulator!');
        terminal.writeln('Эмуляция Linux терминала с базовыми командами.');
        terminal.writeln('Введите \"help\" для списка команд.\r\n');
        updatePrompt();
        
        // Обработка ввода
        terminal.onData(handleInput);
        
        // Обработка изменения размера
        window.addEventListener('resize', () => fitAddon.fit());
        
        function handleInput(data) {
            const code = data.charCodeAt(0);
            
            if (code === 13) { // Enter
                executeCommand(currentCommand);
                currentCommand = '';
                historyIndex = -1;
            } 
            else if (code === 127) { // Backspace
                if (currentCommand.length > 0) {
                    terminal.write('\b \b');
                    currentCommand = currentCommand.slice(0, -1);
                }
            }
            else if (code === 9) { // Tab - автодополнение
                autoComplete();
            }
            else if (code === 27) { // Escape sequences (стрелки)
                if (data.length > 2) {
                    if (data.charCodeAt(1) === 91) {
                        const arrowCode = data.charCodeAt(2);
                        if (arrowCode === 65) { // Стрелка вверх
                            navigateHistory(-1);
                        } else if (arrowCode === 66) { // Стрелка вниз
                            navigateHistory(1);
                        } else if (arrowCode === 67) { // Стрелка вправо
                            // Можно добавить функциональность
                        } else if (arrowCode === 68) { // Стрелка влево
                            // Можно добавить функциональность
                        }
                    }
                }
            }
            else if (code >= 32 && code <= 126) { // Печатные символы
                terminal.write(data);
                currentCommand += data;
            }
        }
        
        function navigateHistory(direction) {
            if (commandHistory.length === 0) return;
            
            if (direction === -1 && historyIndex < commandHistory.length - 1) {
                historyIndex++;
            } else if (direction === 1 && historyIndex > 0) {
                historyIndex--;
            } else if (direction === 1 && historyIndex === 0) {
                historyIndex = -1;
                clearCurrentLine();
                currentCommand = '';
                return;
            } else {
                return;
            }
            
            clearCurrentLine();
            currentCommand = commandHistory[historyIndex];
            terminal.write(currentCommand);
        }
        
        function clearCurrentLine() {
            terminal.write('\r\x1b[K'); // Возврат в начало и очистка строки
            updatePrompt();
        }
        
        function autoComplete() {
            const parts = currentCommand.split(' ');
            const lastPart = parts[parts.length - 1];
            
            if (lastPart) {
                const suggestions = getAutoCompleteSuggestions(lastPart);
                if (suggestions.length === 1) {
                    const completion = suggestions[0];
                    const toAdd = completion.substring(lastPart.length);
                    terminal.write(toAdd);
                    currentCommand += toAdd;
                } else if (suggestions.length > 1) {
                    terminal.write('\r\n');
                    suggestions.forEach(suggestion => terminal.writeln(suggestion));
                    updatePrompt();
                    terminal.write(currentCommand);
                }
            }
        }
        
        function getAutoCompleteSuggestions(partial) {
            const commands = ['ls', 'cd', 'cat', 'pwd', 'whoami', 'date', 'echo', 'mkdir', 'touch', 'rm', 'clear', 'help'];
            const currentDir = getCurrentDirectory();
            const files = Object.keys(currentDir || {});
            
            return [...commands, ...files].filter(item => 
                item.startsWith(partial)
            );
        }
        
        function executeCommand(cmd) {
            commandHistory.unshift(cmd);
            if (commandHistory.length > 100) commandHistory.pop();
            
            terminal.write('\r\n');
            
            const parts = cmd.trim().split(' ');
            const command = parts[0];
            const args = parts.slice(1);
            
            switch(command) {
                case 'ls':
                    lsCommand(args);
                    break;
                case 'cd':
                    cdCommand(args);
                    break;
                case 'cat':
                    catCommand(args);
                    break;
                case 'pwd':
                    pwdCommand();
                    break;
                case 'whoami':
                    whoamiCommand();
                    break;
                case 'date':
                    dateCommand();
                    break;
                case 'echo':
                    echoCommand(args);
                    break;
                case 'mkdir':
                    mkdirCommand(args);
                    break;
                case 'touch':
                    touchCommand(args);
                    break;
                case 'rm':
                    rmCommand(args);
                    break;
                case 'clear':
                    clearTerminal();
                    break;
                case 'help':
                    helpCommand();
                    break;
                case '':
                    break;
                default:
                    terminal.writeln(`\x1b[31mbash: ${command}: команда не найдена\x1b[0m`);
            }
            
            if (command !== 'clear') {
                updatePrompt();
            }
        }
        
        function lsCommand(args) {
            const currentDir = getCurrentDirectory();
            if (!currentDir) {
                terminal.writeln('\x1b[31mОшибка: директория не существует\x1b[0m');
                return;
            }
            
            const items = Object.keys(currentDir);
            if (items.length === 0) {
                terminal.writeln('(пусто)');
                return;
            }
            
            items.forEach(item => {
                const isDir = typeof currentDir[item] === 'object';
                const color = isDir ? '\x1b[34m' : '\x1b[32m';
                terminal.writeln(`${color}${item}${isDir ? '/' : ''}\x1b[0m`);
            });
        }
        
        function cdCommand(args) {
            if (args.length === 0) {
                currentPath = '/home/user';
                return;
            }
            
            const targetPath = resolvePath(args[0]);
            const targetDir = getDirectory(targetPath);
            
            if (targetDir && typeof targetDir === 'object') {
                currentPath = targetPath;
            } else {
                terminal.writeln(`\x1b[31mcd: ${args[0]}: No such directory\x1b[0m`);
            }
        }
        
        function catCommand(args) {
            if (args.length === 0) {
                terminal.writeln('\x1b[31mUsage: cat <file>\x1b[0m');
                return;
            }
            
            const filePath = resolvePath(args[0]);
            const fileContent = getFileContent(filePath);
            
            if (fileContent !== null) {
                terminal.writeln(fileContent);
            } else {
                terminal.writeln(`\x1b[31mcat: ${args[0]}: No such file\x1b[0m`);
            }
        }
        
        function pwdCommand() {
            terminal.writeln(currentPath);
        }
        
        function whoamiCommand() {
            terminal.writeln('guest');
        }
        
        function dateCommand() {
            terminal.writeln(new Date().toString());
        }
        
        function echoCommand(args) {
            terminal.writeln(args.join(' '));
        }
        
        function mkdirCommand(args) {
            if (args.length === 0) {
                terminal.writeln('\x1b[31mUsage: mkdir <directory>\x1b[0m');
                return;
            }
            
            const currentDir = getCurrentDirectory();
            const dirName = args[0];
            
            if (!currentDir[dirName]) {
                currentDir[dirName] = {};
                terminal.writeln(`Создана директория: ${dirName}`);
            } else {
                terminal.writeln(`\x1b[31mmkdir: cannot create directory '${dirName}': File exists\x1b[0m`);
            }
        }
        
        function touchCommand(args) {
            if (args.length === 0) {
                terminal.writeln('\x1b[31mUsage: touch <file>\x1b[0m');
                return;
            }
            
            const currentDir = getCurrentDirectory();
            const fileName = args[0];
            
            if (!currentDir[fileName]) {
                currentDir[fileName] = '';
                terminal.writeln(`Создан файл: ${fileName}`);
            }
        }
        
        function rmCommand(args) {
            if (args.length === 0) {
                terminal.writeln('\x1b[31mUsage: rm <file>\x1b[0m');
                return;
            }
            
            const currentDir = getCurrentDirectory();
            const fileName = args[0];
            
            if (currentDir[fileName]) {
                delete currentDir[fileName];
                terminal.writeln(`Удалено: ${fileName}`);
            } else {
                terminal.writeln(`\x1b[31mrm: cannot remove '${fileName}': No such file\x1b[0m`);
            }
        }
        
        function helpCommand() {
            terminal.writeln('\x1b[36mДоступные команды:\x1b[0m');
            terminal.writeln('  ls [dir]    - список файлов');
            terminal.writeln('  cd [dir]    - сменить директорию');
            terminal.writeln('  cat <file>  - показать содержимое файла');
            terminal.writeln('  pwd         - текущая директория');
            terminal.writeln('  whoami      - информация о пользователе');
            terminal.writeln('  date        - текущая дата и время');
            terminal.writeln('  echo <text> - вывод текста');
            terminal.writeln('  mkdir <dir> - создать директорию');
            terminal.writeln('  touch <file>- создать файл');
            terminal.writeln('  rm <file>   - удалить файл');
            terminal.writeln('  clear       - очистить терминал');
            terminal.writeln('  help        - эта справка');
        }
        
        // Вспомогательные функции для файловой системы
        function resolvePath(path) {
            if (path.startsWith('/')) {
                return path;
            }
            
            const currentParts = currentPath.split('/').filter(p => p);
            const pathParts = path.split('/').filter(p => p);
            
            for (const part of pathParts) {
                if (part === '..') {
                    if (currentParts.length > 0) currentParts.pop();
                } else if (part !== '.') {
                    currentParts.push(part);
                }
            }
            
            return '/' + currentParts.join('/');
        }
        
        function getCurrentDirectory() {
            return getDirectory(currentPath);
        }
        
        function getDirectory(path) {
            const parts = path.split('/').filter(p => p);
            let current = fileSystem;
            
            for (const part of parts) {
                if (current[part] && typeof current[part] === 'object') {
                    current = current[part];
                } else {
                    return null;
                }
            }
            
            return current;
        }
        
        function getFileContent(filePath) {
            const parts = filePath.split('/').filter(p => p);
            const fileName = parts.pop();
            const dirPath = '/' + parts.join('/');
            const directory = getDirectory(dirPath);
            
            return directory && directory[fileName] && typeof directory[fileName] === 'string' 
                ? directory[fileName] 
                : null;
        }
        
        function updatePrompt() {
            const dirName = currentPath.split('/').pop() || '/';
            terminal.write(`\x1b[32mguest\x1b[0m@\x1b[34mbash-emulator\x1b[0m:\x1b[33m${dirName}\x1b[0m$ `);
        }
        
        // Глобальные функции для кнопок
        function clearTerminal() {
            terminal.clear();
            updatePrompt();
        }
        
        function showHelp() {
            terminal.write('\r\n');
            helpCommand();
            updatePrompt();
        }
        
        function insertCommand(cmd) {
            currentCommand = cmd;
            terminal.write('\r' + '\x1b[K'); // Очистить текущую строку
            updatePrompt();
            terminal.write(cmd);
        }
    </script>
</body>
</html>
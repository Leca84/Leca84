<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Терминал xterm.js на GitHub Pages</title>
    <link rel="stylesheet" href="https://unpkg.com/xterm/css/xterm.css">
    <style>
        body {
            margin: 0;
            padding: 20px;
            background-color: #1e1e1e;
            color: #fff;
            font-family: 'Courier New', monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        h1 {
            color: #4CAF50;
            margin-bottom: 10px;
        }
        .container {
            width: 90%;
            max-width: 900px;
        }
        #terminal {
            border: 1px solid #444;
            border-radius: 5px;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        .info {
            background-color: #2d2d2d;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .warning {
            color: #ff9800;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Терминал xterm.js</h1>
        
        <div class="info">
            <p>Это демонстрация терминала на основе xterm.js, размещенного на GitHub Pages.</p>
            <p class="warning">Внимание: Это эмуляция терминала в браузере. Команды выполняются локально и не имеют доступа к вашему серверу.</p>
        </div>
        
        <div id="terminal"></div>
    </div>

    <script src="https://unpkg.com/xterm/lib/xterm.js"></script>
    <script src="https://unpkg.com/xterm-addon-fit/lib/xterm-addon-fit.js"></script>
    <script>
        // Инициализация терминала
        const terminal = new Terminal({
            cursorBlink: true,
            theme: {
                background: '#1e1e1e',
                foreground: '#ffffff',
                cursor: '#4CAF50'
            }
        });
        
        const fitAddon = new FitAddon.FitAddon();
        terminal.loadAddon(fitAddon);
        
        terminal.open(document.getElementById('terminal'));
        fitAddon.fit();
        
        // Обработка изменения размера окна
        window.addEventListener('resize', () => {
            fitAddon.fit();
        });
        
        // Эмуляция команд терминала
        let commandHistory = [];
        let historyIndex = -1;
        let currentCommand = '';
        
        terminal.write('Добро пожаловать в терминал xterm.js!\r\n');
        terminal.write('Доступные команды: help, clear, echo, date, whoami\r\n');
        terminal.write('$ ');
        
        terminal.onData((data) => {
            const code = data.charCodeAt(0);
            
            // Обработка нажатия Enter
            if (code === 13) {
                processCommand(currentCommand);
                currentCommand = '';
                historyIndex = -1;
            } 
            // Обработка нажатия Backspace
            else if (code === 127) {
                if (currentCommand.length > 0) {
                    terminal.write('\b \b');
                    currentCommand = currentCommand.slice(0, -1);
                }
            }
            // Обработка стрелки вверх
            else if (code === 27 && data.length > 1 && data.charCodeAt(1) === 91) {
                if (data.charCodeAt(2) === 65 && commandHistory.length > 0) { // Стрелка вверх
                    if (historyIndex < commandHistory.length - 1) {
                        historyIndex++;
                        // Очистка текущей строки
                        terminal.write('\r$ ');
                        for (let i = 0; i < currentCommand.length; i++) {
                            terminal.write(' ');
                        }
                        terminal.write('\r$ ');
                        
                        currentCommand = commandHistory[historyIndex];
                        terminal.write(currentCommand);
                    }
                } 
                // Обработка стрелки вниз
                else if (data.charCodeAt(2) === 66 && commandHistory.length > 0) { 
                    if (historyIndex > 0) {
                        historyIndex--;
                        // Очистка текущей строки
                        terminal.write('\r$ ');
                        for (let i = 0; i < currentCommand.length; i++) {
                            terminal.write(' ');
                        }
                        terminal.write('\r$ ');
                        
                        currentCommand = commandHistory[historyIndex];
                        terminal.write(currentCommand);
                    } else if (historyIndex === 0) {
                        historyIndex = -1;
                        // Очистка текущей строки
                        terminal.write('\r$ ');
                        for (let i = 0; i < currentCommand.length; i++) {
                            terminal.write(' ');
                        }
                        terminal.write('\r$ ');
                        currentCommand = '';
                    }
                }
            }
            // Обработка обычных символов
            else if (code >= 32 && code <= 126) {
                terminal.write(data);
                currentCommand += data;
            }
        });
        
        function processCommand(command) {
            commandHistory.unshift(command);
            if (commandHistory.length > 50) {
                commandHistory.pop();
            }
            
            terminal.write('\r\n');
            
            // Обработка команд
            const parts = command.trim().split(' ');
            const cmd = parts[0].toLowerCase();
            const args = parts.slice(1);
            
            switch(cmd) {
                case 'help':
                    terminal.write('Доступные команды:\r\n');
                    terminal.write('  help     - показать эту справку\r\n');
                    terminal.write('  clear    - очистить терминал\r\n');
                    terminal.write('  echo     - вывести текст\r\n');
                    terminal.write('  date     - показать текущую дату и время\r\n');
                    terminal.write('  whoami   - показать информацию о пользователе\r\n');
                    break;
                    
                case 'clear':
                    terminal.clear();
                    break;
                    
                case 'echo':
                    terminal.write(args.join(' ') + '\r\n');
                    break;
                    
                case 'date':
                    const now = new Date();
                    terminal.write(now.toString() + '\r\n');
                    break;
                    
                case 'whoami':
                    terminal.write('Пользователь: Гость (это эмуляция терминала)\r\n');
                    break;
                    
                case '':
                    // Пустая команда - ничего не делать
                    break;
                    
                default:
                    terminal.write(`Команда "${cmd}" не найдена. Введите "help" для списка команд.\r\n`);
            }
            
            terminal.write('$ ');
        }
    </script>
</body>
</html>

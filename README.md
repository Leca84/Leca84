<html>
<head>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/jquery.terminal/js/jquery.terminal.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jquery.terminal/css/jquery.terminal.min.css">
</head>
<body>
    <div id="terminal"></div>
    <script>
        $('#terminal').terminal(function(command) {
            if (command === 'help') {
                this.echo('Available commands: ls, cd, pwd, echo');
            } else if (command === 'ls') {
                this.echo('file1.txt\nfile2.txt\ndocuments/');
            } else {
                this.echo('Command not found: ' + command);
            }
        }, {
            greetings: 'Bash Emulator v1.0',
            prompt: 'user@gh-pages:$ '
        });
    </script>
</body>
</html>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WebContainer-like среда на GitHub Pages</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background-color: #1e1e1e;
            color: #fff;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        iframe {
            width: 100%;
            height: 600px;
            border: 1px solid #444;
            border-radius: 5px;
        }
        .info {
            background-color: #2d2d2d;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .warning {
            color: #ff9800;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Альтернатива WebContainer на GitHub Pages</h1>
        
        <div class="info">
            <p class="warning">Внимание: Нативный WebContainer API не работает на GitHub Pages.</p>
            <p>Вместо этого используем встроенную среду StackBlitz:</p>
        </div>
        
        <iframe src="https://stackblitz.com/edit/node-7j9hgy?embed=1" frameborder="0"></iframe>
    </div>
</body>
</html>
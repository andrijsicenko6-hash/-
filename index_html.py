<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 Викторина в Telegram</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            min-height: 100vh;
            padding: 20px;
            color: white;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }
        
        .header {
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #ffd700;
        }
        
        .game-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 15px;
            margin: 15px 0;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
            backdrop-filter: blur(5px);
        }
        
        .game-card:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: #ffd700;
            transform: translateY(-5px);
        }
        
        .btn {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            margin: 10px;
            width: 100%;
            max-width: 300px;
        }
        
        .question-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
            backdrop-filter: blur(5px);
        }
        
        .answer-btn {
            background: rgba(255, 255, 255, 0.15);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .answer-btn:hover {
            background: rgba(255, 255, 255, 0.25);
        }
        
        .timer {
            height: 10px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            margin: 20px 0;
            overflow: hidden;
        }
        
        .timer-bar {
            height: 100%;
            background: #ffd700;
            width: 100%;
        }
        
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Главное меню -->
        <div id="mainMenu">
            <div class="header">
                <h1>🎮 Викторина</h1>
                <p>Проверьте свои знания!</p>
            </div>
            
            <div class="game-card" onclick="startGame()">
                <h2>⚡ Быстрая игра</h2>
                <p>5 вопросов на время</p>
            </div>
            
            <div class="game-card" onclick="showCategories()">
                <h2>🎯 Выбор темы</h2>
                <p>Вопросы по категориям</p>
            </div>
            
            <button class="btn" onclick="Telegram.WebApp.close()">
                ❌ Закрыть
            </button>
        </div>
        
        <!-- Игра -->
        <div id="gameScreen" class="hidden">
            <div class="header">
                <h2 id="questionCounter">Вопрос 1/5</h2>
                <p id="scoreDisplay">Очки: 0</p>
            </div>
            
            <div class="timer">
                <div class="timer-bar" id="timerBar"></div>
            </div>
            
            <div class="question-box">
                <h3 id="questionText">Какой город является столицей России?</h3>
                
                <div id="answersContainer">
                    <div class="answer-btn" onclick="checkAnswer('Москва')">Москва</div>
                    <div class="answer-btn" onclick="checkAnswer('Санкт-Петербург')">Санкт-Петербург</div>
                    <div class="answer-btn" onclick="checkAnswer('Казань')">Казань</div>
                    <div class="answer-btn" onclick="checkAnswer('Новосибирск')">Новосибирск</div>
                </div>
            </div>
            
            <button class="btn" onclick="showMainMenu()">
                ← Назад
            </button>
        </div>
        
        <!-- Категории -->
        <div id="categoryScreen" class="hidden">
            <div class="header">
                <h2>📚 Выберите тему</h2>
            </div>
            
            <div class="game-card" onclick="startCategory('general')">
                <h3>🎯 Общие знания</h3>
            </div>
            
            <div class="game-card" onclick="startCategory('science')">
                <h3>🔬 Наука</h3>
            </div>
            
            <div class="game-card" onclick="startCategory('history')">
                <h3>🏛️ История</h3>
            </div>
            
            <button class="btn" onclick="showMainMenu()">
                ← Назад
            </button>
        </div>
    </div>

    <script>
        // Инициализация Telegram WebApp
        Telegram.WebApp.ready();
        Telegram.WebApp.expand();
        
        let score = 0;
        let currentQuestion = 1;
        let timer = null;
        let timeLeft = 30;
        
        // Вопросы для демо
        const questions = [
            {
                question: "Столица России?",
                correct: "Москва",
                answers: ["Москва", "Санкт-Петербург", "Казань", "Новосибирск"]
            },
            {
                question: "Сколько планет в Солнечной системе?",
                correct: "8",
                answers: ["7", "8", "9", "10"]
            },
            {
                question: "Кто написал 'Войну и мир'?",
                correct: "Лев Толстой",
                answers: ["Достоевский", "Чехов", "Толстой", "Тургенев"]
            }
        ];
        
        // Навигация
        function showMainMenu() {
            document.getElementById('mainMenu').classList.remove('hidden');
            document.getElementById('gameScreen').classList.add('hidden');
            document.getElementById('categoryScreen').classList.add('hidden');
        }
        
        function showGameScreen() {
            document.getElementById('mainMenu').classList.add('hidden');
            document.getElementById('gameScreen').classList.remove('hidden');
            document.getElementById('categoryScreen').classList.add('hidden');
        }
        
        function showCategories() {
            document.getElementById('mainMenu').classList.add('hidden');
            document.getElementById('gameScreen').classList.add('hidden');
            document.getElementById('categoryScreen').classList.remove('hidden');
        }
        
        // Начало игры
        function startGame() {
            score = 0;
            currentQuestion = 1;
            showGameScreen();
            loadQuestion(0);
        }
        
        function startCategory(category) {
            score = 0;
            currentQuestion = 1;
            showGameScreen();
            loadQuestion(0);
        }
        
        // Загрузка вопроса
        function loadQuestion(index) {
            if (index >= questions.length) {
                endGame();
                return;
            }
            
            const q = questions[index];
            document.getElementById('questionCounter').textContent = `Вопрос ${index + 1}/${questions.length}`;
            document.getElementById('scoreDisplay').textContent = `Очки: ${score}`;
            document.getElementById('questionText').textContent = q.question;
            
            // Очищаем контейнер с ответами
            const container = document.getElementById('answersContainer');
            container.innerHTML = '';
            
            // Добавляем кнопки ответов
            q.answers.forEach(answer => {
                const btn = document.createElement('div');
                btn.className = 'answer-btn';
                btn.textContent = answer;
                btn.onclick = () => checkAnswer(answer, q.correct);
                container.appendChild(btn);
            });
            
            // Запускаем таймер
            startTimer();
        }
        
        // Таймер
        function startTimer() {
            clearInterval(timer);
            timeLeft = 30;
            const timerBar = document.getElementById('timerBar');
            timerBar.style.width = '100%';
            
            timer = setInterval(() => {
                timeLeft--;
                const percent = (timeLeft / 30) * 100;
                timerBar.style.width = percent + '%';
                
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    // Время вышло
                    currentQuestion++;
                    if (currentQuestion <= questions.length) {
                        loadQuestion(currentQuestion - 1);
                    } else {
                        endGame();
                    }
                }
            }, 1000);
        }
        
        // Проверка ответа
        function checkAnswer(answer, correct) {
            clearInterval(timer);
            
            const buttons = document.querySelectorAll('.answer-btn');
            buttons.forEach(btn => {
                btn.style.pointerEvents = 'none';
                if (btn.textContent === correct) {
                    btn.style.background = '#4CAF50';
                } else if (btn.textContent === answer && answer !== correct) {
                    btn.style.background = '#f44336';
                }
            });
            
            // Начисляем очки
            if (answer === correct) {
                const bonus = Math.floor(timeLeft);
                score += 100 + bonus;
                alert(`✅ Правильно! +${100 + bonus} очков`);
            } else {
                alert(`❌ Неправильно! Правильный ответ: ${correct}`);
            }
            
            // Переход к следующему вопросу
            setTimeout(() => {
                currentQuestion++;
                if (currentQuestion <= questions.length) {
                    loadQuestion(currentQuestion - 1);
                } else {
                    endGame();
                }
            }, 1500);
        }
        
        // Завершение игры
        function endGame() {
            Telegram.WebApp.showAlert(`🏆 Игра завершена!\n\nВы набрали: ${score} очков\n\nСыграйте еще раз!`);
            showMainMenu();
        }
        
        // Инициализация
        showMainMenu();
    </script>
</body>
</html>

// game.js
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let birdY = canvas.height / 2;
let birdVelocity = 0;
let gravity = 0.5;
let jumpStrength = -10;
let score = 0;

// ลูปเกม
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // ล้างหน้าจอ

    birdVelocity += gravity;  // แรงโน้มถ่วง
    birdY += birdVelocity;

    // ทำให้นกกระโดดเมื่อกด space
    window.addEventListener('keydown', (event) => {
        if (event.code === 'Space') {
            birdVelocity = jumpStrength;
        }
    });

    // ตรวจสอบนกไม่ให้อยู่เหนือหรือใต้จอ
    if (birdY <= 0) birdY = 0;
    if (birdY >= canvas.height - 50) birdY = canvas.height - 50;

    // วาดนก
    ctx.fillStyle = 'yellow';
    ctx.fillRect(50, birdY, 50, 50);  // ตัวนก

    // วาดคะแนน
    ctx.font = "25px Arial";
    ctx.fillStyle = "white";
    ctx.fillText("Score: " + score, 10, 30);

    // เรียกฟังก์ชันเกมลูปใหม่
    requestAnimationFrame(gameLoop);
}

gameLoop();

let perguntas = [
  {
    q: "Qual país é conhecido por criar o sushi?",
    a: ["Japão", "China", "Coreia", "Tailândia"],
    c: 0
  },
  {
    q: "O que é indispensável na feijoada tradicional?",
    a: ["Feijão preto", "Feijão branco", "Lentilha", "Grão de bico"],
    c: 0
  },
  {
    q: "Qual desses cortes é mais fino?",
    a: ["Julienne", "Brunoise", "Cubos", "Meia-lua"],
    c: 0
  }
];

let index = 0;
let acertos = 0;

function carregarPergunta() {
  const box = document.getElementById("quiz-box");
  const p = perguntas[index];

  box.innerHTML = `
    <h3>${p.q}</h3>
    ${p.a.map((alt, i)=>`
      <button class="alt-btn" onclick="responder(${i})">${alt}</button>
    `).join("")}
  `;
}

function responder(i) {
  if (i === perguntas[index].c) acertos++;
  document.getElementById("nextBtn").style.display = "block";
}

function proximaPergunta() {
  index++;
  if (index >= perguntas.length) {
    document.getElementById("quiz-box").innerHTML =
      `<h3>Você acertou ${acertos} de ${perguntas.length} perguntas!</h3>`;
    document.getElementById("nextBtn").style.display = "none";
    return;
  }
  document.getElementById("nextBtn").style.display = "none";
  carregarPergunta();
}

window.onload = carregarPergunta;

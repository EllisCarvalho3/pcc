function buscarReceitas() {
  const ing = document.getElementById("ingredientes").value.trim();
  
  if (!ing) {
    alert("Digite ao menos um ingrediente!");
    return;
  }

  // redireciona para a página de busca (o backend vai tratar isso)
  window.location.href = "/buscar?i=" + encodeURIComponent(ing);
}

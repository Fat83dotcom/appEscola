const dados = document.getElementById('mostra')
dados.style.display = 'none'
const checkDados = document.getElementById('mostraDados')
setInterval(() => {
    if (checkDados.checked) {
        dados.style.display = 'flex'
    }
    else{
        dados.style.display = 'none'
    }
}, 1);
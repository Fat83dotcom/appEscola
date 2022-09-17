const dados = document.getElementById('mostra')
const paginacao = document.getElementById('paginacao')
dados.style.display = 'none'
const checkDados = document.getElementById('mostraDados')
setInterval(() => {
    if (checkDados.checked) {
        dados.style.display = 'flex'
        paginacao.style.display = 'flex'
    }
    else{
        dados.style.display = 'none'
        paginacao.style.display = 'none'
    }
}, 1);
const dados = document.getElementById('mostra')
const checkEnd = document.getElementById('mostraEnd')
setInterval(() => {
    if (checkEnd.checked) {
        dados.style.display = 'block'
    }
    else{
        dados.style.display = 'none'
    }
}, 1);
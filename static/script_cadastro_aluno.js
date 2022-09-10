const enderecos = document.getElementById('mostra')
const checkEnd = document.getElementById('mostraEnd')
setInterval(() => {
    if (checkEnd.checked) {
        enderecos.style.display = 'block'
    }
    else{
        enderecos.style.display = 'none'
    }
}, 1);
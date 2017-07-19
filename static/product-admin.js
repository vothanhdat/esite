
window.addEventListener('DOMContentLoaded',function(){

    $ = django.jQuery;
    var tabcontainer = document.createElement('div')
    var elements = [...$('form > div > fieldset, form > div > .inline-group')]
    var tabs = elements.map(e => document.createElement('a'))
    var pretabs = elements[0]
    var hash = location.hash

    tabcontainer.className = 'admin-tabs'

    function tabonclick(index){
        for(var i in elements){
            console.log(index == i)
            if (i == index){
                tabs[i].classList.add('tab-active')
                elements[i].style.display = 'block'
            }else{
                tabs[i].classList.remove('tab-active')
                elements[i].style.display = 'none'
            }
        }

    }
    
    for (var i in elements) {
        var e = elements[i]
        var h2 = $(e).find('h2')[0]
        var error = $(e).find('.errors') [0]
        var tab = tabs[i]
        tab.href='#tab-' + i
        if(error)
            tab.dataset.error = true

        tab.onclick = tabonclick.bind(e,i)
        if (h2) {
            tab.innerText = h2.innerText
        }else if(i == 0){
            tab.innerText = 'Main'
        }else{
            tab.innerText = 'Tab ' + i
        }
        tabcontainer.appendChild(tab)
    }


    var activeIndex = tabs.findIndex(e => e.href.includes(hash)) 

    if(activeIndex == -1)
        activeIndex = 0;
    console.log({activeIndex})
    tabs[activeIndex].onclick()
    
    $('#product_form > div').prepend(tabcontainer)

})

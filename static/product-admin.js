



function tabLayoutProduct(){

    var tabcontainer = document.createElement('div')
    var elements = [...document.querySelectorAll('form > div > fieldset, form > div > .inline-group')]
    var tabs = elements.map(e => document.createElement('a'))
    var pretabs = elements[0]
    var hash = location.hash

    tabcontainer.className = 'admin-tabs'

    function tabonclick(event){
        var index = this.dataset.index || 0

        for(var i in elements){

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
        var tab = tabs[i]

        var h2 = e.querySelector('h2')
        var error = e.querySelector('.errors,.errornote,.errorlist')


        tab.href='#tab-' + i
        tab.dataset.index=i

        if(error)
            tab.dataset.error = true

        tab.onclick = tabonclick

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

    tabs[activeIndex].onclick()

    var formContainer = document.querySelector('#product_form > div')
    
    if(formContainer.firstChild)
        formContainer.insertBefore(tabcontainer,formContainer.firstChild);
    else
        formContainer.appendChild(childNode);

}

function inlineTabLayout(){
    var formContainer = document.querySelector('.productoption-inline > .djn-items')
    var formContainerBefore = formContainer.querySelector('.djn-no-drag')
    var addItemLink =  document.querySelector('.productoption-inline > .add-item > a')



    var tabcontainer = document.createElement('div')
    var elements = [...document.querySelectorAll('.productoption-inline > .djn-items >.djn-item.djn-inline-form.inline-related')]
    var tabs = []
    var tabs_index = 0;
    
    tabcontainer.className = 'prodoption-tabs'
    
    
    function tabonclick(event){
        var index = this.dataset.index || 0
        for(var i in elements){
            if (i == index){
                tabs[i].classList.add('tab-active')
                elements[i].style.display = 'block'
            }else{
                tabs[i].classList.remove('tab-active')
                elements[i].style.display = 'none'
            }
        }
        tabs_index = index
    }


    function deletenewclick(e){

        elements = [...document.querySelectorAll('.productoption-inline > .djn-items >.djn-item.djn-inline-form.inline-related')]
        
        for(var e of tabs)
            e.remove()
        tabs = []
        
        for (var i in elements)
            createTabBut(i)
        

        if(tabs[tabs_index])
            tabs[tabs_index].onclick()
        else if (tabs[tabs_index - 1])
            tabs[tabs_index - 1].onclick()
        else if(tabs[0])
            tabs[0].onclick()


    }

    function tabnewclick(){
        if(addItemLink.click){
            addItemLink.click()
            elements = [...document.querySelectorAll('.productoption-inline > .djn-items >.djn-item.djn-inline-form.inline-related')]
            
            var newIndex = elements.length - 1
            createTabBut(newIndex);
            tabs[newIndex] && tabs[newIndex].onclick()

            var deleteLink = elements[newIndex].querySelector('h3 > span > a.inline-deletelink')

            console.log({deleteLink})
            if(deleteLink && !deleteLink.__click__){
                deleteLink.addEventListener('click',deletenewclick)
                deleteLink.__click__ = true
            }

        }
        
    }

    

    var newTabInlineOption =  document.createElement('a')
    newTabInlineOption.onclick = tabnewclick
    newTabInlineOption.innerText = 'New Option'
    newTabInlineOption.className = 'tab-new'
    tabcontainer.appendChild(newTabInlineOption)

    function createTabBut(index){
        var e = elements[index]
        var tab = tabs[index] = document.createElement('a')
        var h3 = e.querySelector('h3 > span')
        var error = e.querySelector('.errors,.errornote,.errorlist')
        

        tab.dataset.index = index
        tab.onclick = tabonclick

        if(error)
            tab.dataset.error = true
        
        if (h3) {
            tab.innerText = h3.innerText
        }else{
            tab.innerText = 'Option'
        }

        tabcontainer.insertBefore(tab,newTabInlineOption)

    }

    
    for (var i in elements) {
        createTabBut(i)
    }


    
    tabs[0] && tabs[0].onclick()
    



    formContainer.classList.add('productoption-inline-container')
    
    formContainer.insertBefore(tabcontainer,formContainerBefore);
    
}

window.addEventListener('DOMContentLoaded',function(){
    tabLayoutProduct()
    inlineTabLayout()
})

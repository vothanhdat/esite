console.log('CustomSlug')


$(document).ready(function(){
    function slugify(text)
    {
      return text.toString().toLowerCase()
        .replace(/\s+/g, '-')           // Replace spaces with -
        .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
        .replace(/\-\-+/g, '-')         // Replace multiple - with single -
        .replace(/^-+/, '')             // Trim - from start of text
        .replace(/-+$/, '');            // Trim - from end of text
    }

    var allSlugField = [...document.querySelectorAll('[data-slug]')]
    var allSlugSource = allSlugField.map(e => document.querySelector(`[name=${e.dataset.slugdes}]`))

    var slugsourcecallback =function(slugfield,slugsource){
        console.log('change')
        if(slugsource.value && (!slugfield.value || slugfield.slugauto)){
            slugfield.slugauto = true
            slugfield.isauto = true
            slugfield.value = slugify(slugsource.value)
            slugfield.isauto = false
            
        }
    }

    var slugfieldcallback = function(slugfield,slugsource){
        if(!slugfield.isauto){
            slugfield.slugauto = false
        }
    }
              
    for(var i in allSlugSource){
        if(allSlugSource[i] && allSlugField[i]){
            var slugfield = allSlugField[i]
            var slugsource = allSlugSource[i]

            var callback = slugsourcecallback.bind(null,slugfield,slugsource)


            slugsource.addEventListener("input", callback)
            slugfield.addEventListener("input", slugfieldcallback.bind(null,slugfield,slugsource))

            callback()
        }
    }
    console.log({allSlugField,allSlugSource})
})
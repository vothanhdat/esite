


!function(){
    var __jquery__ = null;
    
    
    function getJquery() {
        return (window.django || {}).jQuery || __jquery__;
    }
    
    Object.defineProperty(window, '$', {
        get: getJquery,
        set(value){
            if(value)
                __jquery__ || (__jquery__ = value);
        }
    });
    
    Object.defineProperty(window, 'jQuery', {
        get: getJquery,
        set(value){
            if(value)
                __jquery__ || (__jquery__ = value);
        }
    });
}()


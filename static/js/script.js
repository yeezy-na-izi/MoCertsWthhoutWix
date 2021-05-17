
 window.addEventListener('DOMContentLoaded', function()  {
    
    'use strict'

    var menu = document.querySelector('.menu-wrap'),
    menuItem = document.querySelectorAll('.menu-link'),
    hamburger = document.querySelector('.header__hamburger');
    
    console.log (menu);
    console.log (menuItem);
    console.log (hamburger);
    
    hamburger.addEventListener('click', function()  {
    hamburger.classList.toggle('hamburger_active');
    menu.classList.toggle('top_active');
    
    });
    
    for (var i=0; i < menuItem.length; i++) {
      var element = menuItem[i];
      console.log (element);
        element.addEventListener('click', function(){
        hamburger.classList.toggle('hamburger_active');
        menu.classList.toggle('top_active');
      });
    };

    $('.EN').click(function(){
        $('.select-list').toggle();
        $('.arrow').toggleClass('rotate');
    
    })
    

}); 
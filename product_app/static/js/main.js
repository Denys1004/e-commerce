
// slideToggle() Show All Categories
$('#slideToggle #show_all').click(function(){
  console.log("You've pressed Show All paragraph");
  $('#slideToggle #hidden_categories').slideToggle(); 
  if ($("#slideToggle #show_all").html() == 'Show all'){
      $("#slideToggle #show_all").html('Hide all');
  }else{
      $("#slideToggle #show_all").html('Show all');
  }
})



// hamburger menu
const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');
    burger.addEventListener('click', () => {
      nav.classList.toggle('nav-active');
      navLinks.forEach((link, index) => {
        if (link.style.animation) {
          link.style.animation = '';
        } else {
          link.style.animation = `navLinkFade 0.4s ease forwards ${index / 20}s`;
        }
      });
      burger.classList.toggle('toggle');
    });
  }
  navSlide();





// scroll to top
// const btnScrollToTop = document.querySelector("#btnScrollToTop");
// btnScrollToTop.addEventListener("click", function () {
//   $("html, body").animate({ scrollTop: 0 }, "slow");
// });


// $(window).scroll(function() {
//     if ($(this).scrollTop()) {
//         $('#scroll-arrow:hidden').stop(true, true).fadeIn();
//     } else {
//         $('#scroll-arrow').stop(true, true).fadeOut();
//     }
// });



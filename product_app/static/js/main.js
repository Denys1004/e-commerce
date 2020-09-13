
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



// Product hover
$('.product_container .product').hover(function(){
  let frontImgAddress = $(this).children('a').children('img').attr('src');
  let backImgAddress = $(this).children('a').children('img').attr('alternative_src');
  $(this).children('a').children('img').attr('src', backImgAddress);
  $(this).children('a').children('img').attr('alternative_src', frontImgAddress);
})

$('.product_container .product').hover(function(){
  $(this).children('.product_description').slideDown();
}, function(){
  $(this).children('.product_description').slideUp(); 
})



// cart page, update qty
$("body").on('change','.qty',(function() {
    var quantity=$(this).val();
    var product_id=$(this).attr('product_id');
    $.ajax({
        url: `${product_id}/update_quantity`,
        method: 'POST',
        data: {
            qty: quantity,
            csrfmiddlewaretoken: csrftoken
        },
        success:(result)=>{
            console.log(result);
            $('#display_products').html(result)
            $.ajax({
              url: '/qty_of_cart_items',
              method: 'GET',
              success:(result) =>{
                $('#cart_number').html(result)
              }
            })
        }
    })
  }))


//category ajax
$("body").on('click','.category_link',(function(e) {
    e.preventDefault()
    var category_id=$(this).attr('category_id')
    $.ajax({
        url:`/display_category/${category_id}`,
        method:'GET',
        success:(response)=>{
            $('.product_container').html(response)
        }
    })
    
}))

//add to cart
$('body').on('click', '.add_to_cart', (function(e) {
    e.preventDefault()
    var product_id=$(this).attr('product_id')
    $(this).html('Added')
    $(this).css('color', '#28a745')
    $.ajax({
        url:`/add_to_cart/${product_id}`,
        method:'GET',
        success:(response)=>{
            $('#cart_number').html(response)
        }
    })
    
}))

//remove category
$("body").on('click','#remove_category',(function(e) {
    e.preventDefault()
    $.ajax({
        url:$(this).attr('href'),
        method:'GET',
        success:(response)=>{
            console.log(response);
            $('#product_categories').html(response)
        }
    })
}))

$("body").on('click','#delete_product_photo',(function(e) {
    e.preventDefault()
    $.ajax({
        url:$(this).attr('href'),
        method:'GET',
        success:(response)=>{
            console.log(response);
            $('.cur_product_images').html(response)
        }
    })
}))


// Carousel
$('.carousel').carousel({
  interval: 3000
})


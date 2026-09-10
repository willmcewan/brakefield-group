(function(){"use strict";
var y=document.getElementById("yr"); if(y) y.textContent=new Date().getFullYear();

var burger=document.getElementById("burger"), mnav=document.getElementById("mobilenav");
if(burger&&mnav){
  burger.addEventListener("click",function(){
    var open=mnav.classList.toggle("open");
    burger.setAttribute("aria-expanded",open?"true":"false");
    burger.setAttribute("aria-label",open?"Close menu":"Open menu");
  });
}
var reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// gameday: gray out past games, mark the next one
var today=new Date(); today.setHours(0,0,0,0); var found=false;
Array.prototype.forEach.call(document.querySelectorAll(".gd-row[data-date]"),function(row){
  var p=row.getAttribute("data-date").split("-");
  var d=new Date(+p[0],+p[1]-1,+p[2]);
  if(d<today) row.classList.add("past");
  else if(!found){ row.classList.add("next"); found=true; }
});

// Reveal on scroll. Deliberately not IntersectionObserver: it never fires in
// some webviews, which would leave sections hidden for good. Polling a rect
// cannot be missed, and a zero-height viewport reveals rather than hides.
var rvEls=Array.prototype.slice.call(document.querySelectorAll(".rv"));
var raf=window.requestAnimationFrame||function(f){return setTimeout(f,16)};
if(reduce){ rvEls.forEach(function(el){el.classList.add("in")}); }
else{
  rvEls.forEach(function(el,i){ el.style.transitionDelay=(Math.min(i,3)*55)+"ms"; });
  var ticking=false,onScroll,poll;
  var stop=function(){clearInterval(poll);window.removeEventListener("scroll",onScroll);window.removeEventListener("resize",onScroll)};
  var check=function(){
    ticking=false;
    var h=window.innerHeight||document.documentElement.clientHeight;
    if(!h){ rvEls.forEach(function(el){el.classList.add("in")}); rvEls.length=0; stop(); return; }
    for(var i=rvEls.length-1;i>=0;i--){
      if(rvEls[i].getBoundingClientRect().top<h*0.92){ rvEls[i].classList.add("in"); rvEls.splice(i,1); }
    }
    if(!rvEls.length) stop();
  };
  onScroll=function(){ if(!ticking){ticking=true;raf(check)} };
  window.addEventListener("scroll",onScroll,{passive:true});
  window.addEventListener("resize",onScroll);
  poll=setInterval(check,200); check();
}

// quote form -> pre-filled email. Swap for a real backend by putting
// action/method on the <form> and deleting this listener.
var form=document.getElementById("quote");
if(form) form.addEventListener("submit",function(e){
  e.preventDefault();
  var v=function(id){var el=document.getElementById(id);return el&&el.value?el.value.trim():"—"};
  var lines=["Name: "+v("name"),"Phone: "+v("phone"),"Email: "+v("email"),"Service: "+v("service"),
    "Date: "+v("date"),"Passengers: "+v("pax"),"Pickup: "+v("from"),"Drop-off: "+v("to"),"","Details:",v("notes")];
  window.location.href="mailto:booking@brakefieldtrans.com?subject="+
    encodeURIComponent("Reservation request — "+v("service")+" — "+v("date"))+
    "&body="+encodeURIComponent(lines.join("\n"));
});
})();
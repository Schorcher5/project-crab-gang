
//Creates nodelist of all items with the .load class

const loading = document.querySelectorForAll(".load");

const options = {
  root:null,
  threshold: 0.1,
}


//Set up observer that switches load class with loaded when tag is observed in the viewport
const observer = new IntersectionObserver(function(entries,observer){
  entries.forEach(entry => { 
      if(entry.isIntersecting){
       entry.target.classList.toggle("loaded");
       observer.unobserve(entry.target);        
      }

    
  });
},options);


//Initializes the observer
loading.forEach(load =>{
  observer.observe(load);
}
                
       

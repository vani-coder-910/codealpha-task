const fromText= document.querySelector(".from-text");
toText= document.querySelector(".to-text");
selectTag = document.querySelectorAll("select");
exchangeIcon = document.querySelector(".exchange");
translateBtn = document.querySelector("button");
icons = document.querySelectorAll(".row i");
selectTag.forEach((tag, id )=> {
   for (const country_code in countries){
       let selected="";
       if(id==0 && country_code=="en-GB"){
        selected="selected";
       }
       else if(id==1 && country_code=="hi-IN"){
        selected="selected";
    }
       let option= `<option  value="${country_code}" ${selected}>${countries[country_code]}</option>`;
       tag.insertAdjacentHTML("beforeend",option );
   }
});

 exchangeIcon.addEventListener("click", ()=>{
   let tempText = fromText.value;
   tempLang = selectTag[0].value;
   fromText.value = toText.value;
   selectTag[0].value = selectTag[1].value;
   toText.value = tempText;
   selectTag[1].value = tempLang;
 });
   translateBtn.addEventListener("click", () => {
    // 1. Make sure you select your input text area correctly (e.g., fromText)
    let text = fromText.value; 
    
    // 2. Properly declare your variables
    let translateFrom = selectTag[0].value;
    let translateTo = selectTag[1].value;
    
    // 3. Construct the API URL
    let apiUrl = `https://api.mymemory.translated.net/get?q=${text}&langpair=${translateFrom}|${translateTo}`;
    
    fetch(apiUrl)
        .then(res => res.json())
        .then(data => {
            console.log(data);
            // Display translatedText: data.responseData.translatedText
            toText.value = data.responseData.translatedText;
        });
});
icons.forEach(icon => {
   icon.addEventListener("click", ({target}) =>{
      if(target.classList.contains("fa-copy")){
         if(target.id =="from"){
            
                navigator.clipboard.writeText(fromText.value);
         }else {
            
            navigator.clipboard.writeText(toText.value);
         }
        
      }
   })
})
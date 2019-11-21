/**************************************************************************************************
JS HELPER FUNCTIONS
**************************************************************************************************/

export default { 
 
   getTitleWords : (original) => {
      let format = original.replace('_', ' ');
      format = format.replace(/\b\w/g, l => l.toUpperCase());
      return format;
   },

   isFloat : (input) => {
      let test = Number(input);
      return !Number.isNaN(test);
   }
}


/**************************************************************************************************
RULES-LOADER PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';

import MenuLayout from '../layouts/menu-layout'




class RuleBook extends React.Component {

   state = {
      rulesData: {},
   }

   componentDidMount() {
      axios({
         url: 'api/game_rules/rulebook_data/',
         method: 'get',
         data: { }
      }).then( success => {
         let updateState = {rulesData: success.data};
         this.setState({...this.state, ...updateState});
         //console.log(this.state);
      }).catch( error => {
         console.log(error);
      });
   }


   render() {

      return (
       
       <div></div>
      );
   }
}

export default RuleBook;

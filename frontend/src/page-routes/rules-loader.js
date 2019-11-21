/**************************************************************************************************
RULES-LOADER PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
import { When } from 'react-if';

import MenuLayout from '../layouts/menu-layout'
import TableWrapper from '../utility/table-wrapper'

class RulesLoader extends React.Component {

   state = {
      rulesTables: [],
      booksPaths: [],
      bookHtml: 'book-html-default', 
   }

   componentDidMount() {

      axios({
         url: 'api/game_rules/table_summary/',
         method: 'get',
         data: { }
      }).then( success => {
         let updateState = {rulesTables: success.data};
         this.setState({...this.state, ...updateState});
         //console.log(this.state);
      }).catch( error => {
         console.log(error);
      });

      axios({
         url: 'api/game_rules/rulebooks_path/',
         method: 'get',
         data: { }
      }).then( success => {
         let updateState = {booksPaths: success.data};
         this.setState({...this.state, ...updateState});
         //console.log(this.state);
      }).catch( error => {
         console.log(error);
      });
   
   }

   loadDbClick = () => {
      axios({
         url: 'api/game_rules/load_db/',
         method: 'post',
         data: { }
      }).then( success => {
         let updateState = {rulesTables: success.data};
         this.setState({...this.state, ...updateState});
      }).catch( error => {
         console.log(error);
      });
   }

   createPDFsClick = () => {
      axios({
         url: 'api/game_rules/create_rulebooks/',
         method: 'post',
         data: { }
      }).then( success => {
         let updateState = {booksPaths: success.data};
         this.setState({...this.state, ...updateState});
      }).catch( error => {
         console.log(error);
      });
   }

   createTestHtml = () => {
      axios({
         url: 'api/game_rules/test_html/',
         method: 'get',
         data: { }
      }).then( success => {
         let updateState = {bookHtml: success.data};
         this.setState({...this.state, ...updateState});
         console.log(success.data);
      }).catch( error => {
         console.log(error);
      });
   }

   render() {

      return (
         <MenuLayout>
            <div className='pure-g outer-spacing'>

               <div className='pure-u-1 inner-spacing'>
                  <div className='page-title'>
                     Game Rules Loader
                  </div>
               </div>
            
               <div className='pure-u-8-24 inner-spacing'>
                  <div className='block-horizontal'>

                     <button onClick={ this.loadDbClick }>Load DB</button>

                     <TableWrapper tableRows={ this.state.rulesTables }></TableWrapper>

                  </div>
               </div>

               <div className='pure-u-8-24 inner-spacing'>
                  <div className='block-horizontal'>

                     <div>
                        <button onClick={ this.createPDFsClick }>Create PDFs</button>
                        <br></br>
                        <button onClick={ this.createTestHtml }>Test HTML</button>
                     </div>

                     <div className='links-container'>
                        <When condition={ this.state.booksPaths.length > 0 && this.state.booksPaths[0].url.length > 0 }>
                        { () => 
                           <a href={ this.state.booksPaths[0].url }>{ this.state.booksPaths[0].title }</a>
                        }
                        </When>
                        <When condition={ this.state.booksPaths.length > 0 }>
                        { () => 
                           <div>{ this.state.booksPaths[0].title } not available</div>
                        }
                        </When>
                     </div>

                  </div>
               </div>

            </div>
         </MenuLayout>
      );
   }
}

export default RulesLoader;

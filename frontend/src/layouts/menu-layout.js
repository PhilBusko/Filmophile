/**************************************************************************************************
MENU LAYOUT
**************************************************************************************************/
import * as React from 'react';
import NavMenu from './nav-menu'
import ContentBlock from './content-block';
import './menu-layout.scss'

class MenuLayout extends React.Component {
   render() {
      return (
         <div className='menu-layout'>

            <div className='nav-column'>
               <div className='fixed-panel'>
                  <NavMenu></NavMenu>
               </div>
            </div>

            <div className='content-column'>
               <ContentBlock>
                  { this.props.children }
               </ContentBlock>
            </div>

         </div>
      );
   }
}

export default MenuLayout;

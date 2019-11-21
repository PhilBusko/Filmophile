/**************************************************************************************************
NAV MENU
**************************************************************************************************/
import React, { Component } from 'react';
import { NavLink } from 'react-router-dom'
import { RoutesConfig } from '../app_main/routes'
import './nav-menu.scss'

class NavMenu extends Component {
   render() {

      return (
         <div className='navigation-wrapper'>
            {
               RoutesConfig.map( (menu, idx) => 
                  <div className='nav-link-container' key={ menu.order }>
                     <NavLink exact to={ menu.path }>{ menu.title }</NavLink>
                  </div> )
            }
         </div>
      );
   }
}

export default NavMenu;

/**************************************************************************************************
NAV MENU
**************************************************************************************************/
import React, { Component } from 'react';
import { NavLink } from 'react-router-dom'
import { RoutesConfig } from '../app_main/routes'
import './nav-menu.scss'

class NavMenu extends Component {
    render() {

        let menuRoutes = RoutesConfig.filter( cfg => cfg.title != 'Admin' );

        return (
            <div className='navigation-wrapper'>
                {
                    menuRoutes.map( (menu, idx) => 
                        <div className='nav-link-container' key={ menu.order }>
                            <div className='moving-border'>
                                <NavLink exact to={ menu.path }>{ menu.title }</NavLink>
                            </div>
                        </div> )
                }

                <div className='hover-group'>
                    <div className='hidden-block'>
                        <div className='nav-link-container'>
                            <div className='moving-border'>
                                <NavLink exact to={ '/admin' }>Admin</NavLink>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        );
    }
}

export default NavMenu;

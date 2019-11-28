/**************************************************************************************************
HOME PAGE
**************************************************************************************************/
import React, { Component } from 'react';
import MenuLayout from '../layouts/menu-layout'

class Introduction extends Component {
    render() {
        return (
            <MenuLayout>
                <div className='outer-spacing'>
                    <div className='inner-spacing page-title'>
                        Phil-mo-phile
                    </div>

                    <div className='inner-spacing block-horizontal' style={{'padding': '0px 20px'}}>
                        Welcome to Phil's Filmophile site. 
                        The goal of this site is to aggregate movies and tv shows from different streaming sources
                        and make them available in one place. 
                        The site was first built for the FlatIron School's Data Science Bootcamp,
                        but it is a dear project to me, and has been expanded since.
                        The site also features a recommendation system which is unlike anything else available
                        on the market.
                    </div>

                </div>
            </MenuLayout>
        ); }
    }

export default Introduction;

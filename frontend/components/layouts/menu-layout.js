/**************************************************************************************************
MENU LAYOUT
**************************************************************************************************/
import * as React from 'react';
import NavMenu from './nav-menu'
import ContentBlock from './content-block';
import './menu-layout.scss'

class MenuLayout extends React.Component {

    navigationBkgd = require('../assets/backgrounds/navigation.png')
    contentBkgd = require('../assets/backgrounds/content.png')

    render() {

        if (Math.random() > 0.5)
            this.navigationBkgd = require('../assets/backgrounds/navigation2.png')

        return (
            <div className='pure-g menu-layout'>
                { /*
                <div className='pure-u-4-24 pure-u-xl-3-24  nav-column'
                    style={{ backgroundImage: "url(" + this.navigationBkgd + ")" }}>
                    <div className='fixed-panel'>
                        <NavMenu></NavMenu>
                    </div>
                </div>

                <div className='pure-u-20-24 pure-u-xl-21-24  content-column'
                    style={{ backgroundImage: "url(" + this.contentBkgd + ")" }}>
                    <ContentBlock>
                        { this.props.children }
                    </ContentBlock>
                    <div style={{ height: '20px' }}></div>
                </div>
                */ }

                <div className='pure-u-4-24 pure-u-xl-3-24  nav-column'>
                    <div className='fixed-panel'>
                        <NavMenu></NavMenu>
                    </div>
                </div>

                <div className='pure-u-20-24 pure-u-xl-21-24  content-column'>
                    <ContentBlock>
                        { this.props.children }
                    </ContentBlock>
                    <div style={{ height: '20px' }}></div>
                </div>

            </div>
        );
    }
}

export default MenuLayout;

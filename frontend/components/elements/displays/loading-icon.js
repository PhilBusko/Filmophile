/**************************************************************************************************
LOADING ICON ELEMENT
**************************************************************************************************/
import * as React from 'react';
//import PropTypes from 'prop-types';
import './loading-icon.scss'

class LoadingIcon extends React.Component {

    loadingIcon = require('../../assets/controls/loading_cat.gif')

    render() {
        return (
            <div className='loading-wrapper center-both'>
                <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
            </div>
        );
    }
}

export default LoadingIcon;


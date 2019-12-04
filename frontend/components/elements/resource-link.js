/**************************************************************************************************
RESOURCE LINK ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import { When } from 'react-if';

//import Helper from '../app_main/helpers'
import './resource-link.scss'

class ResourceLink extends React.Component {

    static propTypes = {
        url: PropTypes.string.isRequired,
        icon: PropTypes.string.isRequired,
        text: PropTypes.string.isRequired,
        isLast: PropTypes.bool, 
    }

    static defaultProps = {
        isLast: false,
    }

    render() {
        return (
            <div className='resource-wrapper'>
                <a href={ this.props.url } className='link-panel' target='blank_'>
                    <img src={ this.props.icon } className='resource-icon' alt='icon'/>
                    <span className='link-format'>{ this.props.text }</span>
                </a>
                <When condition={ !this.props.isLast }>
                { 
                    <span className='separator'>|</span>
                }
                </When>
            </div>
        );
    }
}

export default ResourceLink;

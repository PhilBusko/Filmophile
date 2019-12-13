/**************************************************************************************************
RESOURCE LINK ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import './content-link.scss'

class ContentLink extends React.Component {

    static propTypes = {
        url: PropTypes.string.isRequired,
        text: PropTypes.string.isRequired,
    }

    render() {
        return (
            <span className='link-wrapper'>
                <a href={ this.props.url } className='link-panel' target='blank_'>
                    <span className='link-format'>{ this.props.text }</span>
                </a>
            </span>
        );
    }
}

export default ContentLink;

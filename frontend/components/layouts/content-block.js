/**************************************************************************************************
CONTENT BLOCK COMPONENT
**************************************************************************************************/
import React, { Component } from 'react';
import './content-block.scss'

class ContentBlock extends Component {
   render() {
      return (
         <div className='content-wrapper'>

            { this.props.children }

         </div>
      );
   }
}

export default ContentBlock;

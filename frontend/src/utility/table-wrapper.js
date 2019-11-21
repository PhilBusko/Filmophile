/**************************************************************************************************
TABLE-WRAPPER UTILITY
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import ReactTable from "react-table";
import 'react-table/react-table.css';
import Helper from '../app_main/helpers'
import './table-wrapper.scss'

class TableWrapper extends React.Component {

   state = {
      columnsDef: [],
   };

   // update the internal state when the props come in after the initial render/mount
   componentWillReceiveProps(newProps) {
      let dataProps = newProps.tableRows.length > 0 ? Object.getOwnPropertyNames(newProps.tableRows[0]) : [];
      let updateState = {columnsDef: []};

      dataProps.forEach( prop => {
         let numberClass = Helper.isFloat(newProps.tableRows[0][prop]) ? ' center-text' : '';
         let newCol = {
            Header: Helper.getTitleWords(prop),
            headerClassName: 'table-header' + numberClass,
            accessor: prop,
            className: 'table-text' + numberClass,
            width: this.getColumnWidth(newProps.tableRows, prop),   
         };
         updateState.columnsDef.push(newCol);
      });

      //console.log(updateState.columnsDef);
      this.setState({...this.state, ...updateState});
   }

   render() {
      return (
         <div className='table-wrapper'>
            <ReactTable
               data={ this.props.tableRows }
               columns={ this.state.columnsDef }
               minRows={ 1 }
               showPagination={ false }
               sortable={ false }
               resizable={ false }
            />
         </div>
      );
   }

   getColumnWidth = (dataRows, propName) => {
      let maxLength = propName.length;
      dataRows.forEach( row => {
         if (row[propName].length > maxLength)
            maxLength = row[propName].length;
      });
      
      maxLength += 3;            // some wiggle room
      let factor = 10;           // ballpark given average font sizes
      let width = maxLength * factor
      if (width > 180)
         width = 180;

      return width;     
   }

}

TableWrapper.propTypes = {
   tableRows: PropTypes.arrayOf(PropTypes.object).isRequired,
}

export default TableWrapper;

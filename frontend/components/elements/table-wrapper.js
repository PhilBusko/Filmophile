/**************************************************************************************************
TABLE WRAPPER ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import ReactTable from "react-table";
import 'react-table/react-table.css';
import Helper from '../app_main/helpers'
import './table-wrapper.scss'

class TableWrapper extends React.Component {

    static propTypes = {
        tableRows: PropTypes.arrayOf(PropTypes.object).isRequired,
    }
     
    getColumnsDef = () => {
        let tableRows = this.props.tableRows;
        let dataProps = tableRows.length > 0 ? Object.getOwnPropertyNames(tableRows[0]) : [];
        let columnsDef = []
        if (dataProps.length === 0)
            return []

        dataProps.forEach( prop => {
            let numberClass = Helper.isFloat(tableRows[0][prop]) ? ' center-text' : '';
            let newCol = {
                Header: Helper.getTitleWords(prop),
                headerClassName: 'table-header' + numberClass,
                accessor: prop,
                className: 'table-text' + numberClass,
                width: this.getColumnWidth(tableRows, prop),   
            };
            columnsDef.push(newCol);
        });

        return columnsDef;
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

    render() {
        return (
            <div className='table-wrapper'>
                <ReactTable
                    data={ this.props.tableRows }
                    columns={ this.getColumnsDef() }
                    minRows={ 1 }
                    showPagination={ false }
                    sortable={ false }
                    resizable={ false }
                />
            </div>
        );
    }
}

export default TableWrapper;


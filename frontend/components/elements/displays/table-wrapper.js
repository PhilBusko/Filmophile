/**************************************************************************************************
TABLE WRAPPER ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import { When } from 'react-if';
import ReactTable from "react-table";
import 'react-table/react-table.css';
import LoadingIcon from './loading-icon'
import './table-wrapper.scss'

class TableWrapper extends React.Component {

    static propTypes = {
        tableRows: PropTypes.array.isRequired,
        sizeClass: PropTypes.string.isRequired,
    }

    getTitleWords = (original) => {
        let format = original.replace('_', ' ');
        format = format.replace(/\b\w/g, l => l.toUpperCase());
        return format;
    }

    isFloat = (input) => {
        let test = Number(input);
        return !Number.isNaN(test);
    }

    getColumnsDef = () => {
        let tableRows = this.props.tableRows;
        let dataProps = tableRows.length > 0 ? Object.getOwnPropertyNames(tableRows[0]) : [];
        let columnsDef = []
        if (dataProps.length === 0)
            return []

        dataProps.forEach( prop => {
            let numberClass = this.isFloat(tableRows[0][prop]) ? ' center-text' : '';
            let newCol = {
                Header: this.getTitleWords(prop),
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

                <When condition={ this.props.tableRows.length > 0 }>
                { () =>
                    <ReactTable
                        data={ this.props.tableRows }
                        columns={ this.getColumnsDef() }
                        minRows={ 1 }
                        showPagination={ false }
                        sortable={ false }
                        resizable={ false }
                    />
                }
                </When>
                <When condition={ this.props.tableRows.length == 0 }>
                    <div className={ this.props.sizeClass }>
                        <LoadingIcon/>
                    </div>
                </When>

            </div>
        );
    }
}

export default TableWrapper;


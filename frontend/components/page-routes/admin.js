/**************************************************************************************************
ADMIN PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
import MenuLayout from '../layouts/menu-layout'
import { SelectWrapper, ButtonWrapper } from '../elements'
import { PlotWrapper, TableWrapper } from '../elements'


class Admin extends React.Component {

    state = {
        movieTables: [],
        recommendTables: [],
    }
    
    componentDidMount() {
        let DELAY = 400;

        this.axiosWrapper('api/movies/table_counts/', 'movieTables');
        this.axiosWrapper('api/recommend/table_counts/', 'recommendTables');

        setTimeout( () => {
            //console.log( this.state );
        }, 1000);
    }

    axiosWrapper(relativeUrl, stateVar) {
        axios({
            url: relativeUrl,
        }).then( success => {
            let newState = {};
            newState[stateVar] = success.data;      // force the evaluation of stateVar
            this.setState(newState);
        }).catch( error => {
            console.log(error);
        });    
    }

    loadCsvs = () => {
        document.body.style.cursor = 'wait';
        axios({
            url: 'api/movies/load_csvs/',
        }).then( success => {
            this.axiosWrapper('api/movies/table_counts/', 'movieTables');
        }).catch( error => {
            console.log(error);
        }).finally(function () {
            document.body.style.cursor = '';
        });
    }

    masterMovies = () => {
        document.body.style.cursor = 'wait';
        axios({
            url: 'api/movies/master_movies/',
        }).then( success => {
            this.axiosWrapper('api/movies/table_counts/', 'movieTables');
        }).catch( error => {
            console.log(error);
        }).finally(function () {
            document.body.style.cursor = '';
        });
    }

    deleteMovieTables = () => {
        axios({
            url: 'api/movies/delete_tables/',
        }).then( success => {
            this.axiosWrapper('api/movies/table_counts/', 'movieTables');
        }).catch( error => {
            console.log(error);
        });  
    }

    syntheticScores = () => {
        document.body.style.cursor = 'wait';
        axios({
            url: 'api/recommend/synthetic_scores/',
        }).then( success => {
            this.axiosWrapper('api/recommend/table_counts/', 'recommendTables');
        }).catch( error => {
            console.log(error);
        }).finally(function () {
            document.body.style.cursor = '';
        });
    }

    featuresFile = () => {
        document.body.style.cursor = 'wait';
        axios({
            url: 'api/recommend/features_file/',
        }).then( success => {
            this.axiosWrapper('api/recommend/table_counts/', 'recommendTables');
        }).catch( error => {
            console.log(error);
        }).finally(function () {
            document.body.style.cursor = '';
        });
    }

    trainPredict = () => {
        document.body.style.cursor = 'wait';
        axios({
            url: 'api/recommend/train_predict/',
        }).then( success => {
            this.axiosWrapper('api/recommend/table_counts/', 'recommendTables');
        }).catch( error => {
            console.log(error);
        }).finally(function () {
            document.body.style.cursor = '';
        });
    }

    deleteRecommendTables = () => {
        axios({
            url: 'api/recommend/delete_tables/',
        }).then( success => {
            this.axiosWrapper('api/recommend/table_counts/', 'recommendTables');
        }).catch( error => {
            console.log(error);
        });
    }

    render() {
        return (
            <MenuLayout>
                <div className='pure-g spacing-outer'>
                    <div className='pure-u-1'>
                        <div className='spacing-inner page-title'>
                            Webmaster Dashboard
                        </div>
                    </div>

                    <div className='pure-u-1-5'>
                        <div className='spacing-inner control-island control-outer even-panel'>

                            <div className='control-inner subheading'>
                                Movies Data
                            </div>
                            <div className='panel-new-line'></div>

                            <div className='control-inner'>
                                <ButtonWrapper label='Make Master Movies' updateClick={ this.masterMovies }></ButtonWrapper>
                            </div>
                            <div className='panel-new-line'></div>

                            <div className='control-inner'>
                                <ButtonWrapper label='Load Base CSVs' updateClick={ this.loadCsvs }></ButtonWrapper>
                            </div>
                            <div className='panel-new-line'></div>

                            <div className='control-inner'>
                                <ButtonWrapper label='Delete Movie Tables' updateClick={ this.deleteMovieTables }></ButtonWrapper>
                            </div>

                        </div>
                    </div>

                    <div className='pure-u-1-5'>
                        <div className='spacing-inner control-island control-outer even-panel'>

                            <div className='control-inner subheading'>
                                Recommendation Data
                            </div>
                            <div className='panel-new-line'></div>

                            <div className='control-inner'>
                                <ButtonWrapper label='Synthetic User Scores' updateClick={ this.syntheticScores }></ButtonWrapper>
                            </div>
                            <div className='panel-new-line'></div>

                            <div className='control-inner'>
                                <ButtonWrapper label='Create Features File' updateClick={ this.featuresFile }></ButtonWrapper>
                            </div>
                            <div className='panel-new-line'></div>

                            <div className='control-inner'>
                                <ButtonWrapper label='Train & Predict' updateClick={ this.trainPredict }></ButtonWrapper>
                            </div>
                            <div className='panel-new-line'></div>

                            <div className='control-inner'>
                                <ButtonWrapper label='Delete Recommend Tables' updateClick={ this.deleteRecommendTables }></ButtonWrapper>
                            </div>

                        </div>
                    </div>

                    <div className='pure-u-1-4'>
                        <div className='spacing-inner'>
                            <TableWrapper tableRows={ this.state.movieTables }  title='Movie Tables' sizeClass='tiny-plot'/>
                        </div>
                        <div className='spacing-inner'>
                            <TableWrapper tableRows={ this.state.recommendTables }  title='Recommendation Tables' sizeClass='tiny-plot'/>
                        </div>
                    </div>

                </div>
            </MenuLayout>
        );
    }
}

export default Admin;


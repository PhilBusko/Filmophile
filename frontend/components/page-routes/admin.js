/**************************************************************************************************
ADMIN PAGE
**************************************************************************************************/
import React, { useState, useCallback, useEffect } from 'react';
import axios from 'axios';
import useWebSocket from 'react-use-websocket';

import MenuLayout from '../layouts/menu-layout'
import { SelectWrapper, ButtonWrapper, PlotWrapper, TableWrapper } from '../elements'

import { When } from 'react-if';


const WebsocketWrapper = () => {

    // initialize websocket connection

    const socketUrl = 'ws://' + window.location.host + '/ws/chat/lobby/';
    const [receivedJson, setReceivedJson] = useState({});
    const [sendMessage, lastMessage, readyState, getWebSocket] = useWebSocket(socketUrl);
    const connectionStatus = ['Connecting', 'Open', 'Closing', 'Closed'][readyState];


    // send a new message with data from props

    const message = {
        'type': 'from wrapper',
        'text': 'from wrapper',
        'data': null,
    }
    const messageJson = JSON.stringify(message);

    const handleClickSendMessage = useCallback(() => sendMessage(messageJson), []);




    // triggers when a new message is received

    useEffect(() => {
        if (lastMessage !== null) {
            console.log('received message from: ', getWebSocket().url);
            setReceivedJson(prev => JSON.parse(lastMessage.data));
        }
    }, [lastMessage]);


    return (
        <div>
            
            <div className='control-inner'>
                <ButtonWrapper label='Start Process Websocket' updateClick={ handleClickSendMessage }></ButtonWrapper>
            </div>
            <div className='panel-new-line'></div>

            <When condition={ true }>
                { () =>
                    <div>
                        <div>Text: {receivedJson['text']}</div>
                        <div>Progress: {receivedJson['data']}</div>
                    </div>
                }
            </When>
            
            <div>Connection Status: {connectionStatus}</div>

        </div>
    );
};



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


    // WEBSOCKET

    extractMovieDb = () => {
        //document.body.style.cursor = 'wait';
        axios({
            url: 'api/movies/extract_moviedb/',
        }).then( success => {
            console.log("extract_moviedb success");
            console.log(success);
            //this.axiosWrapper('api/movies/table_counts/', 'movieTables');
        }).catch( error => {
            console.log(error);
        }).finally(function () {
            //document.body.style.cursor = '';
        });
    }

    extractReelgood = () => {
        //document.body.style.cursor = 'wait';
        axios({
            url: 'api/movies/extract_reelgood/',
        }).then( success => {
            console.log("extract_reelgood success");
            console.log(success);
            //this.axiosWrapper('api/movies/table_counts/', 'movieTables');
        }).catch( error => {
            console.log(error);
        }).finally(function () {
            //document.body.style.cursor = '';
        });
    }


    extractImdb = () => {
        //document.body.style.cursor = 'wait';
        axios({
            url: 'api/movies/extract_imdb/',
        }).then( success => {
            console.log("extract_imdb success");
            console.log(success);
            //this.axiosWrapper('api/movies/table_counts/', 'movieTables');
        }).catch( error => {
            console.log(error);
        }).finally(function () {
            //document.body.style.cursor = '';
        });
    }



    // BASIC TABLES

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


    // RENDER

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
                        <div className='spacing-inner control-island control-outer'>


                            <div className='control-inner'>
                                <ButtonWrapper label='Start Process Axios' updateClick={ this.extractReelgood }></ButtonWrapper>
                            </div>
                            <div className='panel-new-line'></div>

                            <div className='control-inner'>
                                <WebsocketWrapper></WebsocketWrapper>
                            </div>
                            
                        </div>
                    </div>
                    <div className='pure-u-1'></div>

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


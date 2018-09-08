import React from 'react';
import ReactDOM from 'react-dom';
import './css/bootstrap.css';
import './index.css';

class EmployeeFinder extends React.Component {

  constructor(props) {
      super(props);
      this.state = {
        shortURLinputValue: '',
        longURLinputValue: '',
        employeeID: '',
        errorMessage: '',
        statusCode: 0
      };
    }

    updateLongInputValue(evt) {
    this.setState({
      longURLinputValue: evt.target.value
    });
    }

    updateShortInputValue(evt) {
    this.setState({
      shortURLinputValue: evt.target.value
    });
  }

  getEmployeeFromURL(url, type){
    if(url === ""){
      this.setState({
        errorMessage: "You need to fill in the " + type + " URI."
      });
    }
    fetch('http://localhost:5000/api/shortenURI/getEmployee/' + encodeURIComponent(url) + "/" + type)
            .then((response) => {
              this.setState({
                statusCode: response.status
              });
              return response.text() }).then((text)=>{
                if(this.state.statusCode === 200){
                this.setState({
                  errorMessage: "",
                  inputValue: "",
                  employeeID: "ID: " + text
                });
              }
              else if(this.state.statusCode === 400){
                this.setState({
                  errorMessage: JSON.parse(text).Message
                  });
              }
              else{
                this.setState({
                  errorMessage: "We're sorry, there seems to be something wrong with this service. Please contact support if the issue persists."
                  });
              }
            })
  }

  render() {
    return (
      <div>
      <h1>Determine the employee which generated the short URL</h1>
      <p>So that you can track which employees have shortened internal URIs for distribution.</p>
      <p>This would probably be behind some kind of authentication, and you could do other things like see all the URIs someone shortened, etc. but you get the idea</p>
      <p> Type in the long URL to find out who generated it <input  style={{"width":"80%"}} value={this.state.longURLinputValue} onChange={evt => this.updateLongInputValue(evt)}/> <button onClick={e => this.getEmployeeFromURL(this.state.longURLinputValue, "long")}>Submit</button></p>
      <p>You would really want to join this ID with an internal table and pull a whole lot more values but you get the idea</p>
      <p style={{"color":"red"}}>{this.state.errorMessage}</p>
      <h2>Employee information</h2>
      <p>{this.state.employeeID} </p>
      </div>
    )
}
}


class UrlShortner extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
        inputValue: '',
        shortURL:'',
        employeeID: '',
        rows: [],
        status: 0,
        errorMessage: '',
        current_short_URIs: new Set()
      };
    }

    updateShortURL(new_url){
      this.setState({
        shortURL: new_url
      });
    }

    getShortURI(long_uri, employee_ID) {
      if(long_uri === ""){
        this.setState({
          errorMessage: 'You need to fill in the URI before you press submit.'
        });
        return;
      }

      if(employee_ID === ""){
        this.setState({
          errorMessage: 'You need to fill in the employee ID before you press submit.'
        });
        return;
      }

      //POST requests just didn't want to work. I could make it work with Postman, and I set the application type to JSON and stringified JSON in the body, but it just didn't work
      fetch('http://localhost:5000/api/shortenURI/' + encodeURIComponent(long_uri) + "/" + encodeURIComponent(employee_ID))
              .then((response) => {
                this.setState({
                  status: response.status
                });
                return response.text() }).then((text)=>{
                if(this.state.status === 200 || this.state.status === 201){ //if success
                this.updateShortURL(text);
                if(!this.state.current_short_URIs.has(text)){
                  this.state.current_short_URIs.add(text);
                  this.state.rows.push(
                    <tr>
                      <td key={long_uri}>{long_uri}</td>
                      <td key={text}>{text}</td>
                    </tr>
                  );
                }
                this.setState({
                inputValue: "",
                errorMessage: ''
                });
              } else if(this.state.status === 400) { //API threw specific error
                  var error_message = JSON.parse(text).Message;
                  this.setState({
                    inputValue: "",
                    errorMessage: "We're sorry, there was an error: " + error_message
                  });
              }
              else{ //some other issue
                this.setState({
                  inputValue: "",
                  errorMessage: "We're sorry, there seems to be something wrong with this service. Please contact support if the issue persists."
                });
              }

              })

    }



    updateInputValue(evt) {
    this.setState({
      inputValue: evt.target.value
    });
  }

  updateemployeeValue(evt){
    this.setState({
      employeeID: evt.target.value
    });
  }

  render() {
    return (
      <div>
<h1>URI Shortner</h1>
<h2>Shorten your URI</h2>
<p>Fill in your employee ID and put in a URI to get a shorter one. This would really be behind some kind of login page with authentication, but you get the idea.</p>
<p> Your employee ID: <input value={this.state.employeeID} onChange={evt => this.updateemployeeValue(evt)}/> </p>
<p>Put your URI in the box below and click submit to get a short version of your URI</p>
<p style={{"color":"red"}}>{this.state.errorMessage}</p>
<input style={{"width":"80%"}} value={this.state.inputValue} onChange={evt => this.updateInputValue(evt)}/> <button onClick={e => this.getShortURI(this.state.inputValue, this.state.employeeID)}>Submit</button>
<h3>Your generated URIs</h3>
<table style={{"width":"100%"}}>
  <tr>
    <th>Long URI</th>
    <th>Short URI</th>
  </tr>
  <tbody>
{this.state.rows}
</tbody>
  </table>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <div>
  <UrlShortner />
  <EmployeeFinder/>
  </div>,
  document.getElementById('root')
);

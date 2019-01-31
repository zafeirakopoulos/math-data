import * as React from "react";
import {log} from "util";


export class SaveJson extends React.Component<any, any> {
    constructor(props: any) {
        super(props);

        this.state = {
            generate: false
        }
    }

    componentWillUpdate() {
        if (this.state.generate) {
            this.setState({generate: false});
            return true;
        } else {
            return false;
        }
    }

    render() {
        return (
            <div>
                <button onClick={this.handleClick}>Generate JSON</button>
                <br/>
                <textarea value={JSON.stringify(this.props.jsonOutput)} readOnly={true}/>
            </div>
        );
    }

    private handleClick = () => {
        console.log('generate json');
        this.setState({generate: true});
    }
}
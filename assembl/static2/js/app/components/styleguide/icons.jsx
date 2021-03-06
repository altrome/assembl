import React from 'react';
import { Link } from 'react-router';
import Glyphicon from '../common/glyphicon';

class Icons extends React.Component {
  render() {
    return (
      <div className="margin-xxl">
        <h2 className="dark-title-2 underline" id="icons" style={{ borderBottom: "1px solid #ccc"}}>ICONS</h2>
        <section>
          <div className="inline padding">
            <span className="assembl-icon-add">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-catch">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-checked">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-discussion">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-edit">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-cancel">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-faq">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-filter">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-profil">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-idea">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-link">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-menu-on">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-message">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-expert">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-pepite">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-plus">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-schedule">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-search">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-search2">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-share">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-delete">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-synthesis">&nbsp;</span>
          </div>
          <div className="inline padding">
            <span className="assembl-icon-mindmap">&nbsp;</span>
          </div>
          <div style={{backgroundColor:"#000", width:"200px"}}>
            <div className="inline padding">
              <Link to="http://www.facebook.com" target="_blank">
                <Glyphicon glyph="facebook" color="white" size={30} desc="Facebook" />
              </Link>
            </div>
            <div className="inline padding">
              <Link to="http://www.linkedin.com" target="_blank">
                <Glyphicon glyph="twitter" color="white" size={30} desc="Twitter" />
              </Link>
            </div>
            <div className="inline padding">
              <Link to="http://www.twitter.com" target="_blank">
                <Glyphicon glyph="linkedin" color="white" size={30} desc="Linkedin" />
              </Link>
            </div>
          </div>
        </section>
        <section>
          <h3 className="dark-title-3">Code</h3>
          <pre>
            &lt;span className="assembl-icon-add black"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-catch white"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-checked grey"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-discussion"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-edit"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-cancel"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-faq"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-filter"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-profil"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-idea"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-link"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-menu-on"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-message"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-expert"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-pepite"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-plus"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-schedule"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-search"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-search2"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-share"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-delete"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-synthesis"&gt;&lt;/span&gt;
          </pre>
          <pre>
            &lt;span className="assembl-icon-mindmap"&gt;&lt;/span&gt;
          </pre>
          <pre>
            <div>&lt;Link to="http://www.facebook.com" target="_blank"&gt;</div>
              <div style={{paddingLeft:`${20}px`}}>&lt;Glyphicon glyph="facebook" color="white" size={30} desc="Facebook"/&gt;</div>
            <div>&lt;/Link&gt;</div>
          </pre>
          <pre>
            <div>&lt;Link to="http://www.linkedin.com" target="_blank"&gt;</div>
              <div style={{paddingLeft:`${20}px`}}>&lt;Glyphicon glyph="linkedin" color="white" size={30} desc="Linkedin"/&gt;</div>
            <div>&lt;/Link&gt;</div>
          </pre>
          <pre>
            <div>&lt;Link to="http://www.twitter.com" target="_blank"&gt;</div>
              <div style={{paddingLeft:`${20}px`}}>&lt;Glyphicon glyph="twitter" color="white" size={30} desc="Twitter"/&gt;</div>
            <div>&lt;/Link&gt;</div>
          </pre>
        </section>
      </div>
    );
  }
}

export default Icons;
import React from "react";
import "./ApplicationCard.css"


function ApplicationCard({application, onStatusChange }){
    return (
        <div className="application-card">
            <h3>Application #{application.id}</h3>
            <p>Job ID: {application.job_id}</p>
            <p>Status: {application.status}</p>
            <p>Next Action: {application.next_action|| "None"}</p>
            <p>Notes: {application.notes ||"None"}</p>
            <div className="application-actions">
                {["saved","applied","interview","rejected","offer"].map((status)=>(
                    <button key = {status} 
                            onClick={()=>onStatusChange(application.id, status)}
                            >
                                {status}
                            </button>
                ))}
            </div>
        </div>

    );

}

export default ApplicationCard;
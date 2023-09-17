/**
 * A map control panel for GeoJSON data layers and base tilesets.
 */

"use client";

import Checkbox from "@/components/Checkbox";
import RadioButton from "@/components/RadioButton";
import { useState } from "react";
import { useSnapshot } from "valtio";
import { useLayers } from "@/hooks/useLayers";
import { baseMapStore, reportStore, layerStore } from "@/states/search";


function MapControlPanel() {

    const baseMapSnap = useSnapshot(baseMapStore);
    const layerSnap = useSnapshot(layerStore);
    const layerActions = useLayers(reportStore.report, layerStore);


    // Intialize panel visiblity
    const [expanded, setExpanded] = useState(true);

    return (
        <div className="w-full max-w-xs mx-auto">

            {/** TITLE */}
            <h5 className="text-center">Select Layers</h5>

            {/** MENU */}
            <div className={`form-control h-0 overflow-hidden items-start ${expanded && "h-auto overflow-auto max-h-full"}`}>

                {/** SECTION DIVIDER */}
                <div className="divider m-0"></div>

                {/** DATA LAYER CHECKBOXES */}
                {layerActions.getToggleOptions().map((option, index) => {
                    return <Checkbox
                        key={index}
                        option={option}
                        checked={layerSnap[option].visible}
                        disabled={!layerSnap[option].hasData}
                        onClick={(e) => layerActions.toggleLayer(e)}
                    />
                })}

                {/** DATA LAYER BULK OPERATION BUTTONS */}
                <div className="justify-center py-2">
                    <button
                        className="btn join-item btn-sm normal-case"
                        onClick={(_) => layerActions.showAllLayers()}
                    >
                        All
                    </button>
                    <button
                        className="btn join-item btn-sm normal-case"
                        onClick={(_) => layerActions.hideAllLayers()}
                    >
                        None
                    </button>
                </div>

                {/** SECTION DIVIDER */}
                <div className="divider m-0"></div>

                {/** BASE MAP RADIO BUTTONS */}
                {Object
                    .entries(baseMapSnap.options)
                    .map(([mapType, settings], index) => (
                        <RadioButton
                            key={index}
                            option={mapType}
                            name={settings.name}
                            isChecked={settings.name == baseMapSnap.selected.name}
                            onChange={(e) => baseMapSnap.setMap(e.target.value)}
                        />
                ))}
            </div>

            {/** MENU TOGGLE BUTTON */}
            <div className="flex justify-center py-2">
                <button
                    className="btn btn-sm normal-case"
                    onClick={() => setExpanded((e) => !e)}
                >
                    {expanded ? "Collapse Menu" : "Show Menu"}
                </button>
            </div>
        </div>
    );
}

export default MapControlPanel;
/**
 * A custom hook for managing DeckGL map viewports.
 */

import { bind } from "@/lib/utils";
import { proxy } from "valtio";
import bbox from "@turf/bbox";
import * as turfHelpers from "@turf/helpers";
import { WebMercatorViewport } from "@deck.gl/core";

class ViewportStore {
    current = {
        width: 500,
        height: 500,
        longitude: -95,
        latitude: 35,
        zoom: 3.5,
        pitch: 0,
        bearing: 0
    }
    
    zoomToGeography(geographies) {

        // Abort if no geographies are provided
        if (!geographies) return;

        // Select target geometry
        let target = geographies.find(g => g.properties.is_target);
        if (!target) return;

        // Extract coordinates from target's geographic bounding box
        let bbox = target.geometry.coordinates[0];
        const boundingBoxCoords = [bbox[2], bbox[4]];

        // Create viewport and fit to new bounding box
        const fittedViewport = new WebMercatorViewport(
            this.current
        );
        const currentLatLonZoom = fittedViewport.fitBounds(
            boundingBoxCoords
        );

        // Update map configuration
        this.current = {
            width: this.current.width,
            height: this.current.height,
            longitude: currentLatLonZoom.longitude,
            latitude: currentLatLonZoom.latitude,
            zoom: currentLatLonZoom.zoom,
            pitch: this.current.pitch,
            bearing: this.current.bearing
        }
    }
}

const useViewportStore = () => {
    return bind(proxy(new ViewportStore()));
};


export { useViewportStore }
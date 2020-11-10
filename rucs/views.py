import json
from flask.views import MethodView
from flask import (g, request, abort)
from rucs.models.house_state import (HouseState, Lighting)

class HouseStateInterface( MethodView ):

  # possible extension: GET value of specific field
  # or embedded item instead of entire document
  def get( self ):
    """
    Get house state
    ---
    tags:
      - house-state
    parameters:
      - schema:
          id: access-token
          in: header
          name: cookie
          required:
            - house_id
          description: "stores access token for demo"
          properties:
            house_id:
              type: string
    responses:
      '200':
        description: returns house state with id house_id
        schema:
          id: HouseState
          required:
            - thermostat
            - lighting
          properties:
            thermostat:
              type: integer
              description: house temperature control value, in Celsius
            lighting:
              type: array
              items:
                schema:
                  allOf:
                    - $ref: '#/definitions/Lighting'
                  id: LightingWithId
                  required:
                    - id
                  properties:
                    id:
                      type: integer
                      description: generated id of the lighting
                        unit, unique but can be reasigned if the unit
                        is deleted
    """
    house_state = HouseState.objects( id = g.house_id )
    return house_state[0].to_json()
  
  def post( self ):
    """
    post new lighting unit with give LABEL and on/off STATE.
    ---
    tags:
      - house-state
    parameters:
      - $ref: '#/definitions/access-token'
      - name: body
        in: body
        description: the lighting unit to be added
        schema:
          id: Lighting
          required:
            - label
            - is_on
          properties:
            label:
              type: string
              description: unique label to describe
                the lighting unit
            is_on:
              type: boolean
              description: boolean power state of the
                lighting unit
    responses:
      '200':
        description: lighting unit added
    """
    """
    Uniqueness condition verified manually  -
    mongodb can only verify uniqueness across a collection, and
    not in a list of embedded documents as a "virtual collection"
   
    """
    house_state = HouseState.objects( id = g.house_id )[0]
    label_new = request.get_json()["label"]
  
    # require unique label of lighting unit
    # todo - custom uniqueness exception class
    for lighting in house_state.lighting:
      if lighting.label == label_new:
        abort(500, description = "lighting unit already exists")
  
    # select new id (find smallest available id)
    id = [ lighting.id for lighting in house_state.lighting ]
    if id == []: id_new = 1
    else:
      id.sort()
      id_new = -1
      i = 0
      while i < len(id) - 1:
        if id[i+1] > id[i] + 1: id_new = id[i] + 1
        i += 1
      if id_new == -1: id_new = id[-1] + 1
  
    # insert new lighting unit
    lighting_new_json = json.dumps( {
      "id": id_new,
      "label": label_new,
      "is_on":  request.get_json()["is_on"]
    } )
    house_state.lighting.append(
      Lighting.from_json( lighting_new_json )
    )
    house_state.save()
    return '"new lighting unit saved posted"'
  
  def delete( self ):
    """
    Delete lighting unit
    ---
    tags:
      - house-state
      - lighting-unit
      - delete
    parameters:
      - $ref: '#/definitions/access-token'
      - name: body
        in: body
        required:
          - id
        properties:
          id:
            description: id of lighting unit to delete
            type: integer
    responses:
      '200':
        description: lighing unit deleted
    """
    house_state = HouseState.objects( id = g.house_id )[0]
    id = request.get_json()["id"]
  
    index = 0
    while index < len(house_state.lighting):
      if house_state.lighting[index]["id"] == id:
        del house_state.lighting[index]
      index += 1
  #  for item in house_state.lighting:
  #    if item["id"] == id: del item
  #    break
  
    house_state.save() 
    return '"operation completed"'
  
  def put( self ):
    """
    Update single value
    Update lighting unit power state, label or thermostat state. \
This specification updates only one key per request \
(in fact, it can also update in a single request the thermostat, \
label & is_on of a single lighting unit, but this is not included \
in the specification).
    ---
    parameters:
      - $ref: '#/definitions/access-token'
      - name: body
        in: body
        schema:
          id: house-state-subgraph-single-value
          description: subgraph of HouseState that uniquely
            identifies a single field for an update operation
          minProperties: 1
          maxProperties: 1
          properties:
            thermostat:
              type: string
              description: vaule in Celsius of new temperature
            lighting:
              type: array
              minItems: 1
              maxItems: 1
              items:
                schema:
                  id: lighting-subgraph-single-value
                  description: subgraph of Lighting that uniquely
                    identifies a single field for an update operation
                  required: id
                  minProperties: 2
                  maxProperties: 2
                  properties:
                    id:
                      type: integer
                      description: id of lighting unit
                    label:
                      type: string
                      description: content of new label
                    on_state:
                      type: boolean
                      description: new power stat of the lighting unit
    responses:
      '200':
        description: value updated  
    """
    """
    todo: the operation is simply to update a subgraph
    of a Mongo document - it seems that it can
    be abstracted to replace all the conditionals used bellow,
    and include also the ability to update any valid subgraph
    of the Mongo document
    **** BUG: uniqueness of labels not enforced on update ****
        to prevent repetitive programming, to fix this
        once the uniqueness validator is moved to a separate
        module
    """
    house_state = HouseState.objects( id = g.house_id )[0]
    house_state_update = request.get_json()
  
    if "thermostat" in house_state_update:
      house_state.thermostat = house_state_update["thermostat"]
  
    if "lighting" in house_state_update:
      lighting_unit_update = house_state_update["lighting"][0]
      id = lighting_unit_update["id"]
      lighting_unit = None
  
      # find the lighting Mongo embedded document with id from
      # the PUT request. Mongo can search accross collections
      # but not embedded documents in a list field.
      for item in house_state.lighting:
        if item["id"] == id:
          lighting_unit = item
      if lighting_unit == None:
        abort(500, ( '{"error": {"message":'
          '"id of lighting unit not found"}}'
        ) )
  
      if "is_on" in lighting_unit_update:
        lighting_unit["is_on"] = lighting_unit_update["is_on"]
  
      if "label" in lighting_unit_update:
        lighting_unit["label"] = lighting_unit_update["label"]
  
    house_state.save()
    return '"house state updated"'

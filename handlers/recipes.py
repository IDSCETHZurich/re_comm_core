#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     handlers/recipes.py
#
#     Copyright 2013 RoboEarth
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
#     \author/s: Mayank Singh
#
#

import user_db
import sys
sys.path.append('..')
from transactions import recipes
from transactions import common

#ROS imports
import roslib; roslib.load_manifest('re_srvs')
from re_srvs import srv


class RecipeHandler(object):
    def set_action_recipe(self, req):
        author = user_db.get_username(req.apiKey)
        if not author:
            return False
        
        result = recipes.set(id_=req.id,
                    class_=req.cls,
                    author=author,
                    description=req.description,
                    recipe=req.recipe)

        if result: return True
        else: return False
    
    def get_action_recipe(self, req):
        result = recipes.get(query=req.recipeUID, format="json", exact=True)
        if result:
            return srv.GetActionRecipeResponse(True, result[0]['recipes'][0]['recipe'])
        else:
            return srv.GetActionRecipeResponse(False, '')
    
    def update_action_recipe(self, req):
        # Check if user is active
        author = user_db.get_username(req.apiKey)
        if not user_db.get_activity(author):
            return False

        # Check if recipe already exists
        ar = recipes.get(query=req.uid, format="json", exact=True)
        if not ar:
            return False


        data = {'description': req.description, 'recipe': req.recipe}
        result = recipes.update(id_=req.uid,
                           author=author,
                           data=data)

        if result: return True
        else: return False
    
    def del_action_recipe(self, req):
        return common.del_element(req.recipeUID, req.apiKey, recipes)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     re_comm.py
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

from handlers import environments, recipes, objects
#ROS imports
import roslib; roslib.load_manifest('re_srvs')
import rospy
from re_srvs import srv


def main():
    rospy.init_node('py_re_comm')
    recipe_handler = recipes.RecipeHandler()
    object_handler = objects.ObjectHandler()
    environment_handler = environments.EnvironmentHandler()
    rospy.Service('/py_re_comm/set_action_recipe', srv.SetActionRecipe, recipe_handler.set_action_recipe)
    rospy.Service('/py_re_comm/get_action_recipe', srv.GetActionRecipe, recipe_handler.get_action_recipe)
    rospy.Service('/py_re_comm/update_action_recipe', srv.UpdateActionRecipe, recipe_handler.update_action_recipe)
    rospy.Service('/py_re_comm/del_action_recipe', srv.DelActionRecipe, recipe_handler.del_action_recipe)
    rospy.Service('/py_re_comm/set_object', srv.SetObject, object_handler.set_object)
    rospy.Service('/py_re_comm/get_object', srv.GetObject, object_handler.get_object)
    rospy.Service('/py_re_comm/update_object', srv.UpdateObject, object_handler.update_object)
    rospy.Service('/py_re_comm/del_object', srv.DelObject, object_handler.del_object)
    rospy.Service('/py_re_comm/set_environment', srv.SetEnvironment, environment_handler.set_environment)
    rospy.Service('/py_re_comm/get_environment', srv.GetEnvironment, environment_handler.get_environment)
    rospy.Service('/py_re_comm/update_environment', srv.UpdateEnvironment, environment_handler.update_environment)
    rospy.Service('/py_re_comm/del_environment', srv.DelEnvironment, environment_handler.del_environment)
    rospy.spin()

if __name__ == "__main__":
    main()
   

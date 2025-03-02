/* @odoo-module */

import {
    Component,
    onWillStart,
    onMounted,
    onWillUnmount,
    useChildSubEnv,
    useRef,
    useState,
    useEffect,
    useExternalListener,
} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class TodolistOWLComponent extends Component{
        static template = 'TodolistTemplate';
        static props = {};
        static components = {};


        setup(){
        this.todoList = useState({tasks:[]})
        this.task = useState({id:null, name:'', color:'#ffffff', completed:false})
        this.orm = useService('orm')

        onWillStart(async () => {
        await this.getALLTask()
        });
        }


       async getALLTask(){
               this.todoList.tasks = await this.orm.searchRead('todo.list', [], ['id','name','color','completed'])
               console.log('tasks------',this.todoList.tasks)
       }

       openEditTaskModal(todo){
       this.task.id = todo.id
       this.task.name = todo.name
       this.task.color = todo.color
       this.task.completed = todo.completed
       }

       openNewTaskModal(){
       this.task.id = null
       this.task.name = ''
       this.task.color = '#ffffff'
       this.task.completed = false
       }

        async saveTask() {
        if (this.task.id) {
            // Update existing task
            await this.orm.write('todo.list', [this.task.id], {
                name: this.task.name,
                color: this.task.color,
                completed: this.task.completed
            });
        } else {
            // Create new task
            const newTaskId = await this.orm.create('todo.list', [{
                name: this.task.name,
                color: this.task.color,
                completed: this.task.completed
            }]);
            this.task.id = newTaskId;
        }
        await this.getALLTask();  // Refresh the list
    }
}

registry.category('actions').add("TodolistOWLComponent",TodolistOWLComponent);
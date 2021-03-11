#include "ADDERNode.h"
#include "Nodes.h"

ADDERNode::ADDERNode() : AbstractNode {"1-ADDER", 2, 2}
{
    // Adopt the convention that the 0th digit is the right most digit and the n+1th digit is the carry bit.
    this->internalNodes.push_back(new XORNode());
    this->internalNodes.push_back(new ANDNode());

    this->getInputPort(0)->connectTo(this->internalNodes[0]->getInputPort(0));
    this->getInputPort(1)->connectTo(this->internalNodes[0]->getInputPort(1));
    this->getInputPort(0)->connectTo(this->internalNodes[1]->getInputPort(0));
    this->getInputPort(1)->connectTo(this->internalNodes[1]->getInputPort(1));

    this->internalNodes[0]->getOutputPort(0)->connectTo(this->getOutputPort(0));
    this->internalNodes[1]->getOutputPort(0)->connectTo(this->getOutputPort(1));
}

ADDERNode::~ADDERNode()
{
    //dtor
}

ADDERNode::ADDERNode(const ADDERNode& other)
{
    //copy ctor
}

ADDERNode& ADDERNode::operator=(const ADDERNode& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}

void ADDERNode::Process(){
    for(int i = 0; i < inputPorts ; i ++){
        this->getInputPort(i)->sendData();
    }

    for(int i = 0; i < (int) this->internalNodes.size(); i ++){
        this->internalNodes[i]->performOperation();
    }

    for(int i = 0; i < outputPorts; i ++){
        this->getOutputPort(i)->receiveData();
    }

}

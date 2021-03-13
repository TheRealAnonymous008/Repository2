#include "REGNode.h"
#include "Nodes.h"

REGNode::REGNode() : AbstractNode {"REG", 3, 1}
{
    // A register takes in 3 parameters, a data bit, a store bit and a clock signal.
    this->internalNodes.push_back(new MUXNode());
    this->internalNodes.push_back(new DFFNode());

    this->getInputPort(0)->connectTo(this->internalNodes[0]->getInputPort(0));
    this->getInputPort(1)->connectTo(this->internalNodes[0]->getInputPort(2));
    this->internalNodes[0]->getOutputPort(0)->connectTo(this->internalNodes[1]->getInputPort(0));
    this->getInputPort(2)->connectTo(this->internalNodes[1]->getInputPort(1));

    this->internalNodes[1]->getOutputPort(0)->connectTo(this->internalNodes[0]->getInputPort(1));
    this->internalNodes[1]->getOutputPort(0)->connectTo(this->getOutputPort(0));
}

REGNode::~REGNode()
{
    //dtor
}

REGNode::REGNode(const REGNode& other)
{
    //copy ctor
}

REGNode& REGNode::operator=(const REGNode& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}

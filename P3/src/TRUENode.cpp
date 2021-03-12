#include "TRUENode.h"
#include "AbstractNode.h"

TRUENode::TRUENode() : AbstractNode {"TRUE", 0, 1}
{

}

TRUENode::~TRUENode()
{
    //dtor
}

TRUENode::TRUENode(const TRUENode& other)
{
    //copy ctor
}

TRUENode& TRUENode::operator=(const TRUENode& rhs)
{
    if (this == &rhs) return *this; // handle self assignment
    //assignment operator
    return *this;
}

void TRUENode::Process(){
    this->outPorts[number]->setRegister(*signal);
    this->outPorts[number]->receiveData();
}

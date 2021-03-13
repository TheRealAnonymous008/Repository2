#ifndef REGNODE_H
#define REGNODE_H

#include <AbstractNode.h>


class REGNode : public AbstractNode
{
    public:
        REGNode();
        virtual ~REGNode();
        REGNode(const REGNode& other);
        REGNode& operator=(const REGNode& other);

    protected:

    private:
};

#endif // REGNODE_H

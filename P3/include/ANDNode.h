#ifndef ANDNODE_H
#define ANDNODE_H

#include <AbstractNode.h>


class ANDNode : public AbstractNode
{
    public:
        ANDNode();
        virtual ~ANDNode();
        ANDNode(const ANDNode& other);
        ANDNode& operator=(const ANDNode& other);

    private:
        void Process() override;

};

#endif // ANDNODE_H
